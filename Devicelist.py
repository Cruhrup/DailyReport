from panos.firewall import Firewall
from panos.panorama import Panorama
from okta.client import Client as OktaClient
from O365 import Account

#Firewalls
firewall01 = Firewall("FW_IP_HERE", api_key="MY_API_KEY_HERE")
firewall02 = Firewall("FW_IP_HERE", api_key="MY_API_KEY_HERE")

#Panorama
panorama01 = Panorama("PANORAMA_IP_HERE", api_key="MY_API_KEY_HERE")

#Okta SDK (PROD ENV)
#Instantiating with a Python dictionary in the constructor
config = {
    'orgUrl': 'https://YOUR_OKTA_ORG_HERE.okta.com',
    #Token expires 30 days without usage
    'token': 'MY_API_TOKEN_HERE'
}
okta_client = OktaClient(config)

#Okta Prod Agents
OKTAAGENT01 = "HOSTNAME_OR_IP_HERE"
OKTAAGENT02 = "HOSTNAME_OR_IP_HERE"


#Device list to run script on
fw_list = [firewall01, firewall02]
panorama_list = [panorama01]
okta_agent_list = [OKTAAGENT01, OKTAAGENT02]

#EMAILER
#grabbing delegated permissions here via scope helper
scopes = ['message_send', 'basic', 'message_send_shared']
credentials = ('Application(Client)_ID_HERE', 'Client_Secret_Value_HERE')
account = Account(credentials, tenant_id='TENANT_ID_HERE', scopes=scopes)

''' Uncomment below 'if' statement to authenticate if no auth token in working dir or auth token expired
if account.authenticate():
    print('Authenticated!')
'''
