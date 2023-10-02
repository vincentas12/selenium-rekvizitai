import requests as r
import urllib3
from bs4 import BeautifulSoup
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
import easyocr
import numpy as np
import time
import urllib.request
import base64
from io import StringIO
from multiprocessing import Pool
from tqdm import tqdm
payload = {
    "_token" : "PbWaGorMN0g74VuUjHh2YPdPPrLFVS5Ol2GR7MXX",
    "gender": "male",
    "lang": "lt_LT"
}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "72",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "XSRF-TOKEN=eyJpdiI6InlwWldZcUNXVWlZT3BlOU5QN0NqUnc9PSIsInZhbHVlIjoiWFAvWjhxUERGM2ZkRW5ZNTNJenhyZk1EUTJaR1cvaWNTaTlEZEEvaUtDaURDVi8rM3Z6YUNHMkhDT1RDbDhyOVpTUWplUHM0TDFrdW5LNFovWkkvS1Q0a2RxWW4vaDVXdjZxNHo5UkR4QldFYVQxcnFwMTQ5aWVSbytJWUZQSzgiLCJtYWMiOiI2OTczNWQ5YzMzNGNiYzQ2ZjRiZWQwNWRiNTMyY2UxNGQ4NWMzNDU0M2Q2MWVlMWRjMGMyZjcyNTQwYTljMmRlIn0%3D; generatefakename_session=eyJpdiI6ImhkVTJzVVlCTE00Mk1qU1ZVV2RMOHc9PSIsInZhbHVlIjoidlBzSklxRGNxRklWc1h4M2lLSHBPTXBnUEViQXk0Zmpwd3l2NDVqMTIxR0NkMGVmb0xHemdJSHUwblZkNkJTRzlQeE56ZHF0NVA3b1IrNlcxQ1BQdFZNdy84RVpybXoyVkhKS1JDU3RmbXZRNjZOUXYyeER3dVlFbnFmRlhRMTgiLCJtYWMiOiI0YjQ0ZjBlMjA1ZmIxZmU2MmM0OThjZDk4YmMzMzkxNmU5ZWExMmQzOTYyMGIwMGE5ZWE5M2YzNTUzZDdhMDAwIn0%3D",
    "Host": "generatefakename.com",
    "Origin": "https://generatefakename.com",
    "Referer": "https://generatefakename.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Brave";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"'
}

def get_tapatybe():
    response = r.post("https://generatefakename.com/generate-name/name", headers=headers,data=payload, verify=False)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find('section', {'class': 'panel'})
    data= soup.find('h3')
    return data.text

def comment():
    urllib3.disable_warnings()

    #chromedriver_path = '/usr/bin/chromedriver'
    options = Options()
    #options.binary_location = '/usr/bin/brave'
    services = Service()
    driver = webdriver.Chrome(options=options, service=services)

    driver.get("https://rekvizitai.vz.lt/imone/mureka/atsiliepimai/?rating=10")
    #time.sleep(1000)
    time.sleep(3)
    cokie = driver.find_element(By.ID, 'cookiescript_close')
    ActionChains(driver).click(cokie).perform()
    tapatybe = get_tapatybe()
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
    al.send_keys("‎‎‎‎‎ ")

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
    reader = easyocr.Reader(['en'], gpu=True)
    text = reader.readtext(image="tet.png")
    pin = (text[0][1]).replace(' ', '')
    al = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div[2]/div/div/form/div[8]/div/div/div/div[1]/input')
    al.send_keys(str(pin).upper())
    time.sleep(1)

    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div[2]/div/div/form/div[10]/div/button')
    button.click()

    foundMessage = False
    id = 0

    numeris = 0
    while not foundMessage and numeris < 15:
        time.sleep(0.5)
        request = r.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={account[0]}&domain={account[1]}")
        data = request.json()
        if len(data) > 0:
            foundMessage = True
            id = data[0]['id']

        numeris += 1

    if numeris < 15:
        mail = r.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={account[0]}&domain={account[1]}&id={id}')
        mail_data = BeautifulSoup(mail.json()['body'], 'lxml')
        mail_data = mail_data.find("a")

        driver.get(mail_data.text)
        time.sleep(1)
        cokie = driver.find_element(By.ID, 'cookiescript_close')
        ActionChains(driver).click(cokie).perform()
        el = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/main/div/div[2]/form/button")
        el.click()

        time.sleep(1)
        print("KOMENTARAS SUBOTINTAS")

def comment_wrapper(_):
    comment()

if __name__ == '__main__':
    n = int(input("Enter the number of bots: "))

    # Use Pool for multiprocessing
    with Pool(n) as pool:
        # Use map to execute comment_wrapper function n times in parallel
        pool.map(comment_wrapper, range(n))
