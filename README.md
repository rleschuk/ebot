### Clone from repository
```
# cd /opt
# git clone https://github.com/rleschuk/ebot.git
# cd ebot
# python3 -m venv venv
# source venv/bin/activate
# pip install -r requirements.txt
# touch .env
# cp deploy/ebot.service /etc/systemd/system/
# systemctl start ebot
# systemctl enable ebot

.env:
--------------------------------------------------------------------
ADMINS=391158244,447734520,195819500,286658949
TOKEN=YOUR_PRODUCTION_BOT_TOKEN
DEV_TOKEN=YOUR_DEVELOPMENT_BOT_TOKEN
HTTPS_PROXY=socks5://user:pass@YOUR_PROXY_IP:1080
LDAP_HOST=YOUR_LDAP_HOST
LDAP_PORT=636
LDAP_USER=YOUR_LDAP_USER
LDAP_PASS=YOUR_LDAP_PASS
LDAP_DOMAIN=YOUR_LDAP_DOMAIN
TAC_USERNAME=YOUR_TAC_USER
TAC_PASSWORD=YOUR_TAC_PASS
PATH=$PATH:$HOME/bin:/usr/lib/oracle/12.1/client64/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/12.1/client64/lib
ORACLE_HOME=/usr/lib/oracle/12.1/client64
TNS_ADMIN=$ORACLE_HOME/network/admin
NSS_SSL_CBC_RANDOM_IV=0
NLS_LANG='.UTF8'
--------------------------------------------------------------------
```

### Updating from repository
```
# cd /opt/ebot
# git pull
# systemctl restart ebot
```
