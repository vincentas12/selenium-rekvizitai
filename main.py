import requests as r
import urllib3
from bs4 import BeautifulSoup
import PIL.Image 
import pyocr 
import pyocr.builders

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random
from scipy.ndimage import gaussian_filter
from PIL import Image, ImageFilter
from scipy import ndimage
import pytesseract
import numpy as np
import time
import urllib.request
import base64
from io import StringIO

urllib3.disable_warnings()

payload = {
    "_token" : "9pM6vTujiVGo2w8mRQtzQL4Ouh7C4LQF2h0oEwus",
    "gender": "male",
    "lang": "lt_LT"
}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "70",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "XSRF-TOKEN=eyJpdiI6Im5IcGlZVnhTZlpsdCt4UjVzY2dZNFE9PSIsInZhbHVlIjoiL2FQRFhmcEk3cWh1V2N0bGdQMjlGajJWRVkxZmMxVEdUNnZWa25VNW1seDF2ekgvT1JKR1EwQjJsQVlnZnF0VFIwczFMMGFzVDdQZS8xR0I5TlpraXg4RWdvMUFmSjNXUlZGL0dXZ1dub2UxNjluckxUbEE3ZG5rNjY1eTVNckYiLCJtYWMiOiJkMmM5OGY1MGIyYjhiZDY2MTkzZmM0N2U3ODQ4NGUxMmJlOTE0ODc3MWZiZGUxMDI5MGVkOWNlZTNlZjdjNDg5In0%3D; generatefakename_session=eyJpdiI6ImNQVU1UN3BzS3VabUNtRkVxcGh4Z1E9PSIsInZhbHVlIjoib05Da25xa3ptcHdQTFBtV0VsWUhPZHlmRDcySGNSajRWdXRpbDdiYXhIUnduKzkxcGdyRnZES0pKWGtSR29JQS9FK3dCMXBnVWVCM3RWY1JwaHczbXFzU0N3TysvV2luQ0NPby9VM3JrVHRDUUpWR2pUR05MelQyZmo4RWhLekoiLCJtYWMiOiI0NWE0MzA3ODE2NDBlZTIwNDUxM2I1MzVlMWVjNGMzN2YyM2ViNzJiMjk2ZWUzNGU4M2RlNjgyNWY0N2ZmNGE1In0%3D",
    "Host": "generatefakename.com",
    "Origin": "https://generatefakename.com",
    "Referer": "https://generatefakename.com/name/random/lt/lt",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Brave\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\""
}
def tapatybe():
    response = r.post("https://generatefakename.com/generate-name/name", headers=headers,data=payload, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    tapatybe = soup.find('section', {'class': 'panel'})
    tapatybe= soup.find('h3')
    tapatybe = tapatybe.text
    return tapatybe
chromedriver_path = '/usr/bin/chromedriver'
options = Options()
options.binary_location = '/usr/bin/brave'
services = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(options=options, service=services)

driver.get("https://rekvizitai.vz.lt/imone/mureka/atsiliepimai/?rating=10")
#time.sleep(1000)
time.sleep(3)
cokie = driver.find_element(By.ID, 'cookiescript_close')
ActionChains(driver).click(cokie)
tapatybe = tapatybe()

requestData = r.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
email = requestData.json()
gmail = email[0]
account = gmail.split("@")
print(gmail)
al = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div[2]/div/div/form/div[3]/div/div/div[1]/input')
al.send_keys(str(tapatybe).split(" ")[0])
al = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div[2]/div/div/form/div[4]/div[1]/div/div[1]/input')
al.send_keys(gmail) # email
al = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div[2]/div/div/form/div[6]/div/div/div[1]/textarea')
al.send_keys("      ")

chaptcha = driver.find_element(By.XPATH, "//*[@id='security_code_image']")
chaptcha.screenshot("chaptcha.png")
# thresold1 on the first stage
th1 = 140
th2 = 140 # threshold after blurring 
sig = 1.5 # the blurring sigma

original = Image.open("chaptcha.png")
black_and_white =original.convert("L") #converting to black and white 
first_threshold = black_and_white.point(lambda p: p > th1 and 255)
first_threshold.save("tet.png")
tools = pyocr.get_available_tools()
image = PIL.Image.open("tet.png")
ocr_tool = tools[0]
text = ocr_tool.image_to_string( image, builder=pyocr.builders.TextBuilder() )
print(text)


time.sleep(1000)
