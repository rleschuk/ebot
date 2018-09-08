
import os
import re
import ldap
from sshtunnel import SSHTunnelForwarder
from utils import Memory

CONTACTS_LDAP_HOST = os.getenv('LDAP_HOST')
CONTACTS_LDAP_PORT = int(os.getenv('LDAP_PORT'))
CONTACTS_LDAP_DOMAIN = os.getenv('LDAP_DOMAIN')
CONTACTS_LDAP_USER = '%s@%s' % (os.getenv('LDAP_USER'), CONTACTS_LDAP_DOMAIN)
CONTACTS_LDAP_PASS = os.getenv('LDAP_PASS')

def init_handler(bot):

    @bot.message_handler(commands=["contact"])
    @bot.message_handler_safe
    @bot.is_private
    @bot.is_logged
    def cmd_contact(message):
        """
        Поиск контактов
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_contact_1)
        bot.register_next_step_handler(msg, proc_contact)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_contact(message):
        bot.log(message)
        bot.send_chat_action(message.chat.id, 'typing')
        pattern = message.text.strip()
        if '@' not in pattern and pattern.startswith('+7'):
            pattern = pattern.replace('-', '').replace(' ', '')
        results = get_contact(pattern)#, ssh_proxy=bot.config.get_ssh_proxy())
        if results:
            for result in results[:3]:
                bot.send_message(message.chat.id, result['msg'], parse_mode='Markdown')
                if result['phone_number'] and re.search('^\+7', result['phone_number']):
                    bot.send_message(message.chat.id, result['phone_number'])
                if result['mobile_number'] != result['phone_number'] and result['mobile_number']:
                    bot.send_message(message.chat.id, result['mobile_number'])
            if len(results) > 3:
                bot.reply_to(message, bot.lang.cmd_contact_2 % len(results))
            return
        bot.reply_to(message, bot.lang.cmd_contact_3)


@Memory.timed(3600)
def get_contact(pattern, ssh_proxy=None):
    results = []

    if re.search(r'^((\+7|8)\d{10}|\d{5,11})$', pattern):
        pattern = re.sub(r'^(\+7|8)', '', pattern)
        pattern = "(|(mobile=*{0})(telephoneNumber=*{0}))".format("*".join(pattern))
    elif re.search(r'^\S+@\S+$', pattern):
        pattern = "(mail={0})".format(pattern)
    else:
        pattern = pattern.replace('ё', 'е')
        pattern = "(&(cn={0}*)(mail=*@*))".format(pattern)

    if ssh_proxy is not None:
        with SSHTunnelForwarder(
            (ssh_proxy.get('host'), ssh_proxy.get('port')),
            ssh_username=ssh_proxy.get('user'),
            ssh_password=ssh_proxy.get('pass'),
            remote_bind_address=(CONTACTS_LDAP_HOST, CONTACTS_LDAP_PORT)
        ) as server:
            local_port = str(server.local_bind_port)
            search = find_in_ldap("ldaps://localhost:%s" % local_port, pattern)
    else:
        search = find_in_ldap("ldaps://%s:%d" % (CONTACTS_LDAP_HOST, CONTACTS_LDAP_PORT), pattern)

    for dn, entry in search[:-1]:
        for key in ['name', 'title', 'department', 'mail', 'company', 'telephoneNumber', 'mobile']:
            entry[key] = entry[key][0].decode('utf8') if key in entry else None

        if not entry['name'] and not entry['title']: continue
        if entry['name']: msg = '*{0}*'.format(entry['name'])
        if entry['title']: msg += '\n{0}'.format(entry['title'])
        if entry['department']: msg += '\n{0}'.format(entry['department'])
        if entry['company']: msg += '\n{0}'.format(entry['company'])
        if entry['mail']: msg += '\nEmail: {0}'.format(entry['mail'])
        phone_number = ''
        mobile_number = ''
        if entry['telephoneNumber']:
            if not re.search('\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d', entry['telephoneNumber']):
                msg += '\nВнутр. номер: {0}'.format(entry['telephoneNumber'])
            if re.search('\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d.*\d', entry['telephoneNumber']):
                phone_number = re.sub('-','',entry['telephoneNumber'])
                phone_number = re.sub('^8','+7',phone_number)
        if entry['mobile']:
            mobile_number = entry['mobile']
            mobile_number = re.sub('-','',mobile_number)
            mobile_number = re.sub('^8','+7',mobile_number)
        results.append({
            'msg': msg,
            'phone_number': phone_number,
            'mobile_number': mobile_number
        })

    return results


def find_in_ldap(url, pattern):
    l = ldap.initialize(url)
    l.protocol_version = ldap.VERSION3
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.simple_bind_s(CONTACTS_LDAP_USER, CONTACTS_LDAP_PASS)
    results = l.search_s(
        ','.join('DC=%s' % dc for dc in CONTACTS_LDAP_DOMAIN.split('.')),
        ldap.SCOPE_SUBTREE,
        pattern,
        ['name', 'title', 'department', 'mail', 'company', 'telephoneNumber', 'mobile']
    )
    l.unbind_s()
    return results
