from panos.firewall import Firewall
from panos.panorama import Panorama
from okta.exceptions import OktaAPIException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import asyncio
import os
import Devicelist


# Time conversion
def timeconvert(n):
    return str(datetime.timedelta(seconds = n))
# Start script execution timer
startTime = datetime.datetime.now()
print('')
print("Starting Now: ", (startTime).strftime("%H:%M:%S"))

print('')
print('============FIREWALL_SECTION_START==============')
print('')

for fw in Devicelist.fw_list:
    sys_info = fw.op('show system info')

    if sys_info.attrib['status'] == 'success':
        #Setting up vars
        show_clock = fw.op('show clock')
        ha = fw.op('show high-availability state')
        mp_cpu = fw.op('show system state filter "sys.monitor.s0.mp.exports"')
        dp_cpu = fw.op('show system state filter "sys.monitor.s1.dp0.exports"')
        gp_usage = fw.op('show global-protect-gateway statistics')
        gp_portal = fw.op('show global-protect-portal summary detail')
        all_tuns = fw.op('show vpn flow')
        tun_a = fw.op('show vpn ipsec-sa')
        #Cleaning vars
        mp_cpu = mp_cpu[0].text
        dp_cpu = dp_cpu[0].text
        ha_state = (f"{ha.find('.//state').text}").capitalize()
        ha_time = int(f"{ha.find('.//state-duration').text}")
        #Setting up tunnel lists
        tun_a_list = []
        tun_i_list = []
        #Cleaning portal name
        try:
            gp_portal_txt = gp_portal.find('result').text
            gp_name = gp_portal_txt.split(' ', 2)[1]
            gp_name = gp_name.splitlines()[0]
        except AttributeError:
            gp_name = None
        #Check if any num_ipsec tunnels exist
        if int(all_tuns[0][1].text) > 0:
            #Grab list of all tunnels configured
            for x in all_tuns.iter('name'):
                #Same logic as active tunnel list if statement
                tun_i_list.append((x.text.split(':', 1)[0]))
                #Convert to set to remove dupes
                tun_i = set(tun_i_list)

            #Grab active tunnel list, if any exist
            if tun_a.iter('entry'):
                for x in tun_a.iter('name'):
                    #Iterate over 'name' attribute in tun_a, kill everything after ':', append to list
                    tun_a_list.append((x.text.split(':', 1)[0]))
                #Convert to set to remove dupes
                tun_set = set(tun_a_list)
                #Convert set to string for prettier formatting
                active_tuns = ', '.join(tun_set)
            else:
                tun_set = {}
                active_tuns = None

            #If tunnel from all tunnels doesn't exist in active_tuns, it's inactive
            inactive_tuns = tun_i.difference(tun_set)
            #Convert set to string for prettier formatting
            inactive_tuns = ', '.join(inactive_tuns)
        else:
            active_tuns = None
            inactive_tuns = None
            
        '''
        mp_cpu is unique and was a PITA
        basically, show system state returns CDATA due to having a bunch of data with random symbols in it
        CDATA is NOT parsed (it is automatic escaping) so it's treated as a long string

        technically could've grabbed dp_cpu in an easier way, but I spent so much time on 
        mp_cpu I may as well get good use out of that method

        active vs inactive tunnels was an incredible feat....
        basically, grab list of all tunnels, grab list of active tunnels
        if tunnel x in all tunnels is NOT in active tunnels, it is inactive
        this is the same logic that Network > IPSec Tunnels > Status follows with the green or red LED.png

        '''

        dyn_up = (f"\n App Version: {sys_info.find('.//app-version').text}"
            f" / {sys_info.find('.//app-release-date').text}"
            f"\n Threat Version: {sys_info.find('.//threat-version').text}"
            f" / {sys_info.find('.//threat-release-date').text}"
            f"\n Antivirus: {sys_info.find('.//av-version').text}"
            f" / {sys_info.find('.//av-release-date').text}"
            f"\n Device Dictionary: {sys_info.find('.//device-dictionary-version').text}"
            f" / {sys_info.find('.//device-dictionary-release-date').text}"
            f"\n Wildfire: {sys_info.find('.//wildfire-version').text}"
            f" / {sys_info.find('.//wildfire-release-date').text}"
            )
        cpu_util = (f"\n MP: {mp_cpu[48:50]}%"
            f"\n DP: {dp_cpu[49:51]}%"
            )
        gp_stats = (f"\n Portal Name: {gp_name}"
            f"\n Current Users: {gp_usage[0].find('TotalCurrentUsers').text}"
            )
        print(f"Hostname: {sys_info.find('.//hostname').text}")
        print(f"Current Time: {(show_clock[0].text).strip()}")
        print(f"Uptime: {sys_info.find('.//uptime').text}")
        print(f"HA State: {ha_state} for {timeconvert(ha_time)}")
        print(f"PANOS Version: {sys_info.find('.//sw-version').text}")
        print(f"IP Address: {sys_info.find('.//ip-address').text}")
        print("CPU Utilization: ", cpu_util)
        print(f"GP: ", gp_stats)
        print("Dynamic Updates: ", dyn_up)
        print("Active Tunnels: \n", active_tuns)
        print("Inactive Tunnels: \n", inactive_tuns)

        if fw in Devicelist.fw_list[:-1]:
            print('')
            print('=======NEXT_FIREWALL======')
            print('')
        else:
            print('')
            print('=============FIREWALL_SECTION_DONE==============')
            print('')
    else:
        print("Error: Please contact the admin for debugging")

print('')
print('============PANORAMA_SECTION_START==============')
print('')

for pa in Devicelist.panorama_list:
    sys_info = pa.op('show system info')

    if sys_info.attrib['status'] == 'success':
        #Setting vars
        devices = pa.op('show devices summary')
        show_clock = pa.op('show clock')
        mp_cpu = pa.op('show system state filter "sys.monitor.s0.mp.exports"')

        #Cleaning vars
        mp_cpu = mp_cpu[0].text
        cpu_util = (f"\n MP: {mp_cpu[48:50]}%")

        '''
        Basically the same stuff as the firewalls, just less because Panorama is MP only unit

        '''

        dyn_up = (f"\n App Version: {sys_info.find('.//app-version').text}"
            f" / {sys_info.find('.//app-release-date').text}"
            f"\n Antivirus: {sys_info.find('.//av-version').text}"
            f" / {sys_info.find('.//av-release-date').text}"
            f"\n Device Dictionary: {sys_info.find('.//device-dictionary-version').text}"
            f" / {sys_info.find('.//device-dictionary-release-date').text}"
            f"\n Wildfire: {sys_info.find('.//wildfire-version').text}"
            f" / {sys_info.find('.//wildfire-release-date').text}"
            )

        print(f"Hostname: {sys_info.find('.//hostname').text}")
        print(f"Current Time: {(show_clock[0].text).strip()}")
        print(f"Connected Devices: {devices.find('.//connected').text}")
        print(f"Disconnected Devices: {devices.find('.//dis-connected').text}")
        print(f"Device Groups In-Sync: {devices.find('./result/device-summary/dg-status/in-sync').text}")
        print(f"Templates In-Sync: {devices.find('./result/device-summary/tpl-status/in-sync').text}")
        print("CPU Utilization: ", cpu_util)
        print("Dynamic Updates: ", dyn_up)

        if pa in Devicelist.panorama_list[:-1]:
            print('')
            print('=================NEXT_PANORAMA==================')
            print('')
        else:
            print('')
            print('=============PANORAMA_SECTION_DONE==============')
            print('')
    else:
        print("Error: Please contact the admin for debugging")

print('')
print('===============OKTA_SECTION_START===============')
print('')

'''
In order for this to work on Windows, you must run 'set PYTHONUTF8=1' before running the script for the first time
This is because Windows still uses legacy encoders, while Mac and Linux use UTF-8
Make sure Chrome Driver is in PATH! We are running headless because eff GUI and we want better performance

'''

try:
    print('====Okta_Health_Check=====\n')
    #Chrome Driver options for performance enhancing, mainly care about headless here
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # chrome_options.headless = True # also works

    url = 'https://status.okta.com/'

    #Create web session and load the page
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    #Wait for the page to fully load
    driver.implicitly_wait(5)

    #Parse HTML code
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    #Grab all divs that have js-subservice class attribute
    service_list = (soup.find_all("div", {"class":"js-subservice"}))

    #Grab overall Okta system status and when the last page update was
    sys_status = (soup.find("div", {"class":"system__status_today_status"}).text)
    sys_update = (soup.find("div", {"class":"system__status_today_update"}).text)

    print(sys_status, ":", sys_update)

    #Iterate through the divs and grab service name + service status
    for x in service_list:
        #'Okta Services'/'Third Party' have diff class names than the rest of the services
        try:
            s_name = (x.find("div", {"class":"sub_service_category_status_name"}).text)
            s_stat = (x.find("div", {"class":"sub_service_category_status_category"}).text)
            print(s_name, ":", s_stat)
        except:
            s_name = (x.find("div", {"class":"sub_service_item_status_name"}).text)
            s_stat = (x.find("div", {"class":"sub_service_item_status_category"}).text)
            print(s_name, ":", s_stat)

    #Close web session
    driver.quit()
except:
    print("Error: Please contact the admin for debugging")

'''
Basically, just followed Okta SDK doc and expanded on that
Asyncio is a really complicated package, so I'm not 100% sure on debugging but I try my best
It does allow for parallel processing which is extremely efficient

'''

try:
    print('\n====Agent_Health_Check====\n')
    for ip in Devicelist.okta_agent_list:
        response = os.popen(f"ping -n 1 {ip}").read()
        if "Received = 1" in response:
            print(f"{ip} is OK!")
        else:
            print(f"{ip} is DOWN. Please check the Okta Admin console.")
except:
    print("Error: Please contact the admin for debugging")

try:
    print('\n====App_Auth_Protocols====\n')
    async def main():
        query_param = {'filter': 'status eq "ACTIVE"',
                    'limit': '200'
            }
        try:
            apps, resp, err = await Devicelist.okta_client.list_applications(query_param)
            auth_mode = []
            for app in apps:
                try:
                    #print(app.sign_on_mode.name)
                    auth_mode.append(app.sign_on_mode.name)
                except:
                    pass
            print("SWA: ", auth_mode.count('AUTO_LOGIN') + auth_mode.count('BROWSER_PLUGIN'))
            print("SAML: ", auth_mode.count('SAML_2_0'))
            print("ODIC: ", auth_mode.count('OPENID_CONNECT'))
            print("Others: ", auth_mode.count('BOOKMARK'))
        except OktaAPIException as err:
            print(err)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except:
    print("Error: Please contact the admin for debugging")

print('')
print('===============OKTA_SECTION_DONE================')
print('')

#Script execution time end
endTime = datetime.datetime.now()
timeDiff = str((endTime - startTime).seconds)
print("Execution Time: ", timeDiff, "seconds")

'''
Future addons: 
Docker containerization, way too many dependencies and want clean reproducability
Auto-email via Outlook
Maybe convert output to csv for formatting?

Requirements:
Pip(3)
panos sdk - pip install pan-os-python
okta sdk - pip install okta
BS4 - pip install beautifulsoup4
html5lib - pip install html5lib
requests - pip install requests
selenium - pip install selenium
Chrome Driver (Version 108.0.5359.71)- https://chromedriver.storage.googleapis.com/index.html?path=108.0.5359.71/

Tested on Python 3.9.13
'''