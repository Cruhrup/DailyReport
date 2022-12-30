# DailyReport
A daily report python script for work that gathers details from Palo Alto firewalls, Panorama, and Okta agents

#### Dependencies
+ panos sdk - pip install pan-os-python

+ okta sdk - pip install okta

+ BS4 - pip install beautifulsoup4

+ html5lib - pip install html5lib

+ requests - pip install requests

+ selenium - pip install selenium

+ Chrome Driver (Tested with Version 108.0.5359.71) - https://chromedriver.storage.googleapis.com/index.html?path=108.0.5359.71/

+ Tested on Python 3.9.13 with Windows 10 21H2 19044.2364

#### Setup
1. Download both the .py files in the repository

2. Generate API keys for your firewalls as well as Panorama using the below link:
https://docs.paloaltonetworks.com/pan-os/10-1/pan-os-panorama-api/get-started-with-the-pan-os-xml-api/get-your-api-key

3. Generate an API key for your Okta org using the below link:
https://developer.okta.com/docs/guides/create-an-api-token/main/

##### Setup - Devicelist.py
1. On section `Firewalls`, replace `FW_IP_HERE` with your firewall IP and `MY_API_KEY_HERE` with your firewall API key

2. On section `Panorama`, replace `PANORAMA_IP_HERE` with your Panorama IP and `MY_API_KEY_HERE` with your Panorama API key

3. Repeat steps 1 and 2 for more firewalls and/or Panoramas per your environment

4. On section `Okta SDK (PROD ENV)`, replace `YOUR_OKTA_ORG_HERE` with your Okta org name (i.e `https://acme.okta.com`) and `MY_API_TOKEN_HERE` with your Okta API token

5. On section `Okta Prod Agents`, replace `HOSTNAME_OR_IP_HERE` with either your Okta agents IP address or hostname (make sure hostname is resolvable via `nslookup`)

6. On section `Device list to run script on`, add or remove the variables you just created in steps 1-5 to their appropriate list

7. Done! To run, open command prompt, navigate to the folder of the script, and execute `python3 Daily_Report.py > Daily_Report.txt`

#### Example Output

<details><summary>Daily_Report.txt</summary>
<p>

```
Starting Now:  11:54:23

============FIREWALL_SECTION_START==============

Hostname: PA-FW01
Current Time: Fri Dec 30 12:54:26 EST 2022
Uptime: 240 days, 15:28:03
HA State: Active for 240 days, 15:18:00
PANOS Version: 10.1.5-h1
IP Address: 10.10.10.1
CPU Utilization:  
 MP:  3%
 DP:  0%
GP:  
 Portal Name: gp.acme.com
 Current Users: 23
Dynamic Updates:  
 App Version: 8659-7774 / 2022/12/28 20:24:22 EST
 Threat Version: 8659-7774 / 2022/12/28 20:24:22 EST
 Antivirus: 4313-4826 / 2022/12/30 07:57:35 EST
 Device Dictionary: 64-365 / 2022/12/15 23:59:07 EST
 Wildfire: 729546-732919 / 2022/12/30 12:12:11 EST
Active Tunnels: 
 aws_s2s_vpn_tun, gcp_s2s_vpn_tun
Inactive Tunnels: 
 azure_s2s_vpn_tun, dc02_s2s_vpn_tun

=======NEXT_FIREWALL======

Hostname: PA-FW02
Current Time: Fri Dec 30 12:54:32 EST 2022
Uptime: 226 days, 12:48:57
HA State: Active for 226 days, 12:37:24
PANOS Version: 10.1.5-h1
IP Address: 10.10.10.2
CPU Utilization:  
 MP:  6%
 DP:  6%
GP:  
 Portal Name: gp.acme2.com
 Current Users: 32
Dynamic Updates:  
 App Version: 8659-7774 / 2022/12/28 20:24:22 EST
 Threat Version: 8659-7774 / 2022/12/28 20:24:22 EST
 Antivirus: 4313-4826 / 2022/12/30 07:57:35 EST
 Device Dictionary: 64-365 / 2022/12/15 23:59:07 EST
 Wildfire: 729546-732919 / 2022/12/30 12:12:11 EST
Active Tunnels: 
 azure_s2s_vpn_tun, dc02_s2s_vpn_tun
Inactive Tunnels: 
 aws_s2s_vpn_tun, gcp_s2s_vpn_tun

=============FIREWALL_SECTION_DONE==============


============PANORAMA_SECTION_START==============

Hostname: Panorama
Current Time: Fri Dec 30 12:54:41 EST 2022
Connected Devices: 2
Disconnected Devices: 0
Device Groups In-Sync: 2
Templates In-Sync: 2
CPU Utilization:  
 MP:  2%
Dynamic Updates:  
 App Version: 8659-7774 / 2022/12/28 20:23:58 EST
 Antivirus: 4313-4826 / 2022/12/30 07:57:35 EST
 Device Dictionary: 64-365 / 2022/12/15 23:59:07 EST
 Wildfire: 729546-732919 / 2022/12/30 12:12:11 EST

=============PANORAMA_SECTION_DONE==============


===============OKTA_SECTION_START===============

====Okta_Health_Check=====

System Operational : Last updated 9:54am PST
Okta Services : Operational
Core Platform : Operational
Access Gateway : Operational
Advanced Server Access : Operational
API Services : Operational
MFA : Operational
Single Sign-On : Operational
Workflows : Operational
OIG Access Certifications : Operational
OIG Access Requests : Operational
OIG Reporting : Operational
Third Party : Operational

====Agent_Health_Check====

OKTAAGENT01 is OK!
OKTAAGENT02 is OK!

====App_Auth_Protocols====

SWA:  2
SAML:  20
ODIC:  4
Others:  1

===============OKTA_SECTION_DONE================

Execution Time:  29 seconds

```

</p>
</details>

#### Future Feature List

- [ ] Fix Devicelist.py API key hardcoding

- [ ] Docker containerization

- [ ] Output in .csv or different format for easier readability

- [ ] Implement emailer for automatic emailing of results
