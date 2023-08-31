import datetime
import time
import xkcd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import Devices as D

# Function for Selenium setup and to take full page screenshot
def take_screenshot(file_name, username, password):
    # Chrome Driver options for performance enhancing, mainly care about headless here
    chrome_options = Options()
    chrome_options.accept_insecure_certs = True # Added due to self signed cert on Grafana server
    chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    #chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)

    # Login to Grafana
    driver.get('https://my-grafana-instance.com:3000/login')
    driver.find_element(By.CLASS_NAME, 'css-1n6y0bv-input-input').send_keys(username) # XPATH is probs better but lazy rn
    driver.find_element(By.ID, 'current-password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'css-1mhnkuh').click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "css-1m01c8l")))

    # Take screenshot 
    # Set viewport size
    driver.maximize_window()
    driver.set_window_rect(width=1920, height=2160)
    time.sleep(10)
    # Take screenshot
    driver.find_element(By.TAG_NAME, 'body').screenshot(file_name)

    driver.quit()

file_name = 'dashboard.png' 
username = D.username
password = D.password

try:
    take_screenshot(file_name, username, password)
except:
    print("Error Taking Screenshot of Grafana: Contact the admin for debugging")

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
    m = D.account.new_message()
    m.to.add(['notarealemail@outlook.com',
        'sampleemail@outlook.com'])
    m.subject = sub
    m.body = bod
    m.attachments.add(["dashboard.png","xkcd.png"])
    m.send()
except:
    print("Error Sending Email: Contact the admin for debugging")
