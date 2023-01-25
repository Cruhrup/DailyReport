from okta.exceptions import OktaAPIException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import pytz
import asyncio
import os
import requests
import xkcd
import Devices

# Open file and write
f = open("DailyReport.txt", "w")

# Time conversion
def timeconvert(n):
    return str(datetime.timedelta(seconds = n))
# Start script execution timer
estz = pytz.timezone('US/Eastern')
timeNow = datetime.datetime.now(estz)
# startTime called at end for time diff to see script execution
startTime = datetime.datetime.now()

f.write('\n')
f.write("Starting Now: " + (timeNow).strftime("%H:%M:%S %Z"))

f.write('\n\n============FIREWALL_SECTION_START==============\n\n')

for fw in Devices.fw_list:
    sys_info = fw.op('show system info')

    if sys_info.attrib['status'] == 'success':
        # Setting up vars
        show_clock = fw.op('show clock')
        ha = fw.op('show high-availability state')
        mp_cpu = fw.op('show system state filter "sys.monitor.s0.mp.exports"')
        dp_cpu = fw.op('show system state filter "sys.monitor.s1.dp0.exports"')
        gp_usage = fw.op('show global-protect-gateway statistics')
        gp_portal = fw.op('show global-protect-portal summary detail')
        all_tuns = fw.op('show vpn flow')
        tun_a = fw.op('show vpn ipsec-sa')
        # Cleaning vars
        mp_cpu = mp_cpu[0].text
        dp_cpu = dp_cpu[0].text
        ha_state = (f"{ha.find('.//state').text}").capitalize()
        ha_time = int(f"{ha.find('.//state-duration').text}")
        # Setting up tunnel lists
        tun_a_list = []
        tun_i_list = []
        # Cleaning portal name
        try:
            gp_portal_txt = gp_portal.find('result').text
            gp_name = gp_portal_txt.split(' ', 2)[1]
            gp_name = gp_name.splitlines()[0]
        except AttributeError:
            gp_name = None
        # Check if any num_ipsec tunnels exist
        if int(all_tuns[0][1].text) > 0:
            # Grab list of all tunnels configured
            for x in all_tuns.iter('name'):
                # Same logic as active tunnel list if statement
                tun_i_list.append((x.text.split(':', 1)[0]))
                # Convert to set to remove dupes
                tun_i = set(tun_i_list)

            # Grab active tunnel list, if any exist
            if tun_a.iter('entry'):
                for x in tun_a.iter('name'):
                    # Iterate over 'name' attribute in tun_a, kill everything after ':', append to list
                    tun_a_list.append((x.text.split(':', 1)[0]))
                # Convert to set to remove dupes
                tun_set = set(tun_a_list)
                # Convert set to string for prettier formatting
                active_tuns = ', '.join(tun_set)
            else:
                tun_set = {}
                active_tuns = None

            # If tunnel from all tunnels doesn't exist in active_tuns, it's inactive
            inactive_tuns = tun_i.difference(tun_set)
            # Convert set to string for prettier formatting
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
        f.write(f"Hostname: {sys_info.find('.//hostname').text}\n")
        f.write(f"Current Time: {(show_clock[0].text).strip()}\n")
        f.write(f"Uptime: {sys_info.find('.//uptime').text}\n")
        f.write(f"HA State: {ha_state} for {timeconvert(ha_time)}\n")
        f.write(f"PANOS Version: {sys_info.find('.//sw-version').text}\n")
        f.write(f"IP Address: {sys_info.find('.//ip-address').text}\n")
        f.write("CPU Utilization: " + cpu_util)
        f.write(f"\nGP: " + gp_stats)
        f.write("\nDynamic Updates: " + dyn_up)
        f.write("\nActive Tunnels: \n" + str(active_tuns))
        f.write("\nInactive Tunnels: \n" + str(inactive_tuns))

        if fw in Devices.fw_list[:-1]:
            f.write('\n\n=======NEXT_FIREWALL======\n\n')
        else:
            f.write('\n\n=============FIREWALL_SECTION_DONE==============\n')
    else:
        f.write("Error in Firewall Section: Contact the admin for debugging")

f.write('\n============PANORAMA_SECTION_START==============\n\n')

for pa in Devices.panorama_list:
    sys_info = pa.op('show system info')

    if sys_info.attrib['status'] == 'success':
        # Setting vars
        devices = pa.op('show devices summary')
        show_clock = pa.op('show clock')
        mp_cpu = pa.op('show system state filter "sys.monitor.s0.mp.exports"')

        # Cleaning vars
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

        f.write(f"Hostname: {sys_info.find('.//hostname').text}\n")
        f.write(f"Current Time: {(show_clock[0].text).strip()}\n")
        f.write(f"Connected Devices: {devices.find('.//connected').text}\n")
        f.write(f"Disconnected Devices: {devices.find('.//dis-connected').text}\n")
        f.write(f"Device Groups In-Sync: {devices.find('./result/device-summary/dg-status/in-sync').text}\n")
        f.write(f"Templates In-Sync: {devices.find('./result/device-summary/tpl-status/in-sync').text}\n")
        f.write("CPU Utilization: " + cpu_util + '\n')
        f.write("Dynamic Updates: " + dyn_up)

        if pa in Devices.panorama_list[:-1]:
            f.write('\n\n=================NEXT_PANORAMA==================\n\n')
        else:
            f.write('\n\n=============PANORAMA_SECTION_DONE==============\n')
    else:
        f.write("Error in Panorama Section: Contact the admin for debugging")

f.write('\n===============OKTA_SECTION_START===============\n\n')

'''
In order for this to work on Windows (I.e no Docker), you must run 'set PYTHONUTF8=1' before running the script
This is because Windows still uses legacy encoders, while Mac and Linux use UTF-8
Make sure Chrome Driver is in PATH! We are running headless because eff GUI and better performance

After getting this contained via Docker, learned that --no-sandbox needed to be turned on otherwise
Chrome would not start properly in the Docker container
'''

try:
    f.write('====Okta_Health_Check=====\n\n')
    # Chrome Driver options for performance enhancing, mainly care about headless here
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    #chrome_options.headless = True # also works

    url = 'https://status.okta.com/'

    # Create web session and load the page
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait for the page to fully load
    driver.implicitly_wait(5)

    # Parse HTML code
    soup = BeautifulSoup(driver.page_source, 'html5lib')

    # Grab all divs that have js-subservice class attribute
    service_list = (soup.find_all("div", {"class":"js-subservice"}))

    # Grab overall Okta system status and when the last page update was
    sys_status = (soup.find("div", {"class":"system__status_today_status"}).text)
    sys_update = (soup.find("div", {"class":"system__status_today_update"}).text)

    f.write(sys_status + ": " + sys_update + '\n')

    # Iterate through the divs and grab service name + service status
    for x in service_list:
        # 'Okta Services'/'Third Party' have diff class names than the rest of the services
        try:
            s_name = (x.find("div", {"class":"sub_service_category_status_name"}).text)
            s_stat = (x.find("div", {"class":"sub_service_category_status_category"}).text)
            f.write(s_name + ": " + s_stat + '\n')
        except:
            s_name = (x.find("div", {"class":"sub_service_item_status_name"}).text)
            s_stat = (x.find("div", {"class":"sub_service_item_status_category"}).text)
            f.write(s_name + ": " + s_stat + '\n')

    # Close web session
    driver.quit()
except:
    f.write("Error in Okta Health Check: Contact the admin for debugging")

'''
Basically, just followed Okta SDK doc and expanded on there ()
Asyncio is a really complicated package, so I'm not 100% sure on debugging but I try my best
It does allow for parallel processing which is extremely efficient

'''

try:
    f.write('\n====Agent_Health_Check====\n\n')
    for ip in Devices.okta_agent_list:
        response = os.popen(f"ping -c 1 {ip}").read()
        if "1 received" in response:
            f.write(f"{ip} is OK!\n")
        else:
            f.write(f"{ip} is DOWN. Please check the Okta Admin console.\n")
except:
    f.write("Error in Okta Agent Health Check: Contact the admin for debugging")

try:
    f.write('\n====App_Auth_Protocols====\n\n')
    async def main():
        query_param = {'filter': 'status eq "ACTIVE"',
                    'limit': '200'
            }
        try:
            apps, resp, err = await Devices.okta_client.list_applications(query_param)
            auth_mode = []
            for app in apps:
                try:
                    auth_mode.append(app.sign_on_mode.name)
                except:
                    pass
            SWA = auth_mode.count('AUTO_LOGIN') + auth_mode.count('BROWSER_PLUGIN')
            f.write("SWA: " + str(SWA) + '\n')
            f.write("SAML: " + str(auth_mode.count('SAML_2_0')) + '\n')
            f.write("ODIC: " + str(auth_mode.count('OPENID_CONNECT')) + '\n')
            f.write("Others: " + str(auth_mode.count('BOOKMARK')) + '\n')
        except OktaAPIException as err:
            f.write(err)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
except:
    f.write("Error In Okta App Protocols: Contact the admin for debugging")

f.write('\n===============OKTA_SECTION_DONE================\n\n')

# Script execution time end
endTime = datetime.datetime.now()
timeDiff = str((endTime - startTime).seconds)
f.write("Execution Time: " + timeDiff + " seconds")
# Close file
f.close()


# Email the report via O365 with QotD and XKCD comic
try:
    # Setting vars for email readiness
    # Make date format textual (i.e January 12, 2023)
    today = datetime.date.today()
    date = str(today.strftime("%B %d, %Y"))
    # Making the get request for quote of the day (qod) src:https://github.com/lukePeavey/quotable
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    data = response.json()
    # Get xkcd comic
    Comic = xkcd.getRandomComic()
    # Output is just pointing where to place the output, and what to call the file via outputFile
    xkcd.Comic.download(Comic, output='/', outputFile='xkcd.png')

    # Sanitize output
    quote=data["content"]
    author=data["author"]
    qod = quote + '\n' + '-' + author
    sub = 'Daily Report | ' + date
    bod = qod

    # Send email
    m = Devices.account.new_message()
    m.to.add(['notarealemail@outlook.com',
        'sampleemail@outlook.com'])
    m.subject = sub
    m.body = bod
    # Files must be in working dir
    m.attachments.add(['DailyReport.txt',
        "xkcd.png"])
    m.send()
except:
    print("Error Sending Email: Contact the admin for debugging")

'''
Requirements:
Pip(3)
Install below using 'pip install '
panos sdk - pan-os-python
okta sdk - okta
BS4 - beautifulsoup4
html5lib
requests
requests-oauthlib
selenium
stringcase
python-dateutil
tzlocal
pytz
O365 - https://github.com/O365/python-o365
xkcd - https://github.com/TC01/python-xkcd

Download and put in working dir (if using lcoal Windows env and not Docker)
Chrome Driver (Version 108.0.5359.71)- https://chromedriver.storage.googleapis.com/index.html?path=108.0.5359.71/

Tested on Python 3.9.13
Tested on Docker 20.10.21
'''
