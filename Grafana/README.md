### Grafana Implementation

![GrafanaScreencap](https://github.com/Cruhrup/DailyReport/assets/79858481/56c983b1-faf2-43a4-a6dc-8bb453528d55)


Installation instructions
1. Set up a TIG (Telegraf InfluxDB Grafana) environment
2. Follow [this](https://github.com/vbarahona/Panos2Grafana) guide to set up SNMP queries to the firewalls via Telegraf as well as the dashboard for Grafana
3. Install the dependencies required: yesoreyeram-infinity-datasource, volkovlabs-rss-datasource, and marcusolsson-dynamictext-panel
4. Edit the Daily Report-Dashboard.json file for your own tags, hostnames, IPs, etc (main ones are in the InfluxDB section, <IP_ADDR_HERE>, and <OKTA_ADMIN_TENANT_HERE>)
5. Import the edited Dashboard.json into your Grafana environment and enjoy!
