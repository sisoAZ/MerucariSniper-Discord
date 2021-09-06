from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep

options = Options()

options.set_headless(True)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def getItems(url):

    # ブラウザを起動する
    driver = webdriver.Chrome(chrome_options=options)

    # ブラウザでアクセスする
    driver.get(url)

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "search-result")))
        sleep(5)
    except Exception:
        print("ERROR getItems")
        return getItems(url)

    # HTMLを文字コードをUTF-8に変換してから取得します。
    body_html = driver.find_element_by_css_selector('#search-result')
    source = body_html.get_attribute('innerHTML')
    if "item-cell-skeleton" in source:
        print("Skeleton Source")
        return getItems(url)
        
    #print(source)

    driver.close()
    driver.quit()

    return source

def getSource(url):

    # ブラウザを起動する
    driver = webdriver.Chrome(chrome_options=options)

    # ブラウザでアクセスする
    driver.get(url)

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "item-info")))
        sleep(2)
    except Exception:
        print("ERROR getSource")
        return getSource(url)

    # HTMLを文字コードをUTF-8に変換してから取得します。
    body_html = driver.find_element_by_xpath("/html/body")
    source = body_html.get_attribute("innerHTML")

    driver.close()
    driver.quit()

    return source