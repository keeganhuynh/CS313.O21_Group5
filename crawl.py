from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def crawl(url):
    driver = webdriver.Firefox()  # or webdriver.Chrome()
    driver.get(url)

    data = {}

    data['market'] = str(url.split('/')[-1])

    try:
        prev_close_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="PREV_CLOSE-value"]'))
        )
        data['previous_close'] = float(prev_close_element.text.replace(',', ''))

        open_value_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="OPEN-value"]'))
        )
        data['open'] = float(open_value_element.text.replace(',', ''))

        volume_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="TD_VOLUME-value"] > fin-streamer'))
        )
        data['volume'] = float(volume_element.text.replace(',', ''))
    finally:
        driver.quit()

    return data

markets = [
    'ACB.VN',
    'BCM.VN',
    'BID.VN',
    'BVH.VN',
    'CTG.VN',
    'FPT.VN',
    'GAS.VN',
    'GVR.VN',
    'HDB.VN',
    'HPG.VN',
    'MBB.VN',
    'MSN.VN',
    'MWG.VN',
    'PLX.VN',
    'POW.VN',
    'SAB.VN',
    'SHB.VN',
    'SSB.VN',
    'SSI.VN',
    'STB.VN',
    'TCB.VN',
    'TPB.VN',
    'VCB.VN',
    'VHM.VN',
    'VIB.VN',
    'VIC.VN',
    'VJC.VN',
    'VNM.VN',
    'VPB.VN',
    'VRE.VN',
]

with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['market', 'previous_close', 'open', 'volume'])
    writer.writeheader()
    for market in markets:
        data = crawl(f'https://finance.yahoo.com/quote/{market}')
        writer.writerow(data)