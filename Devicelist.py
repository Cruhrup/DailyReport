from panos.firewall import Firewall
from panos.panorama import Panorama
from okta.client import Client as OktaClient
from okta.exceptions import OktaAPIException

'''
I know hardcoding API keys is bad practice, working on a better solution
'''

#Firewalls
firewall01 = Firewall("FW_IP_HERE", api_key="MY_API_KEY_HERE")
firewall02 = Firewall("FW_IP_HERE", api_key="MY_API_KEY_HERE")

#Panorama
panorama01 = Panorama("PANORAMA_IP_HERE", api_key="MY_API_KEY_HERE")

#Okta SDK (PROD ENV)
#Instantiating with a Python dictionary in the constructor
config = {
    'orgUrl': 'https://YOUR_OKTA_ORG_HERE.okta.com',
    #crbot token in Okta prod admin expires 30 days without usage
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
