from O365 import Account

#EMAILER
#grabbing delegated permissions here via scope helper
scopes = ['message_send', 'basic', 'message_send_shared']
credentials = ('Application(Client)_ID_HERE', 'Client_Secret_Value_HERE')
account = Account(credentials, tenant_id='TENANT_ID_HERE', scopes=scopes)

''' Uncomment below 'if' statement to authenticate if no auth token in working dir or auth token expired
if account.authenticate():
    print('Authenticated!')
'''

#Grafana Creds
username = 'badplaintextusername'
password = 'badplaintextpassword'
