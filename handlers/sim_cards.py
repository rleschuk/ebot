
from time import sleep
from threading import Thread
from sqlalchemy import create_engine
import pandas as pd
from sshtunnel import SSHTunnelForwarder
from utils import Memory


def init_handler(bot):

    simdata = SimData(ssh_proxy=bot.config.get_ssh_proxy())

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("/sim"))
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_sim(message):
        """
        Информация из реестра по SIM
        """
        bot.log(message)
        if len(message.text.split()) > 1:
            message.text = ' '.join(message.text.split()[1:])
            return proc_sim(message)
        msg = bot.reply_to(message, bot.lang.cmd_sim_1)
        bot.register_next_step_handler(msg, proc_sim)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_sim(message):
        bot.log(message)
        bot.send_chat_action(message.chat.id, 'typing')
        results = simdata.get_sim(message.text)
        if results:
            bot.send_message(message.chat.id,
                '\n\n'.join(bot.lang.cmd_sim_3.format(**result) for result in results[:3]),
                parse_mode='Markdown')
            if len(results) > 3:
                bot.reply_to(message, bot.lang.cmd_sim_4 % len(results))
            return
        bot.reply_to(message, bot.lang.cmd_sim_5)

    @bot.job('cron', hour='*/1')
    def update_simdata():
        simdata.update()


class SimData(object):

    def __init__(self, ssh_proxy=None):
        self._updating = False
        self.ssh_proxy = ssh_proxy
        self.data = pd.DataFrame()
        Thread(target=self.update).start()

    def update(self):
        if self._updating: return
        self._updating = True
        self.data = self.get_data()
        self._updating = False

    def get_data(self, filter=None):
        data = pd.DataFrame()
        if self.ssh_proxy is not None:
            with SSHTunnelForwarder(
                (self.ssh_proxy.get('host'), self.ssh_proxy.get('port')),
                ssh_username=self.ssh_proxy.get('user'),
                ssh_password=self.ssh_proxy.get('pass'),
                remote_bind_address=('188.186.146.1', 1521)
            ) as server:
                local_port = str(server.local_bind_port)
                dburl = "oracle://os_usr:os_usr@127.0.0.1:%s/orange" % local_port
                data = self.excecute_query(dburl, filter)
        else:
            dburl = "oracle://os_usr:os_usr@188.186.146.1:1521/orange"
            data = self.excecute_query(dburl, filter)
        return data

    def get_sim(self, pattern):
        if not self.data.empty:
            items = pd.concat([
                self.data[self.data['phone_number'].str.contains(pattern, regex=True, na=False)],
                self.data[self.data['iccid'].str.contains(pattern, regex=True, na=False)]
            ])
            if not items.empty: return items.fillna('').to_dict(orient='records')
        items = self.get_data(pattern)
        if not items.empty: return items.fillna('').to_dict(orient='records')
        return []

    def excecute_query(self, dburl, filter=None):
        engine = create_engine(dburl)
        filter = "AND (iccid like '%{0}%' OR phone_number like '%{0}%')".format(filter) if filter else ''
        return pd.read_sql_query('''
        SELECT
            area_name, company_name, iccid, operator_name,
            REGEXP_REPLACE(phone_number, '^\+7', '') as phone_number,
            status_name, tariff_name, to_status_date
        FROM os_usr.vw_sim_cards
        WHERE rownum <= 20000 {0}
        '''.format(filter), engine)
