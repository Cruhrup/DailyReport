# Dockerfile, Image, Container
FROM python:3.9

ADD Daily_Report.py .
ADD Devicelist.py .
ADD o365_token.txt .
ADD xkcd.png .

# Install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Install chromedriver (Okta_Health_Check section)
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port to avoid crash
ENV DISPLAY=:99

# Install ping
RUN apt update
RUN apt install iputils-ping -y

# Get script dependencies
RUN pip install pan-os-python okta beautifulsoup4 html5lib requests requests-oauthlib selenium stringcase python-dateutil tzlocal pytz o365 xkcd

CMD ["python3", "./Daily_Report.py"]
