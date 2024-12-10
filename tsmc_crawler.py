from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time


# 配置 ChromeOptions
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1440,768")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


#PS: 請限制瀏覽器 1440x768 的視窗大小來進行以下步驟 步驟1. 前往 台灣證券交易所 頁面 https://www.twse.com.tw/zh/index.html
driver.get("https://www.twse.com.tw/zh/index.html")


actions = ActionChains(driver)

#交易資訊
element = driver.find_element(By.XPATH, "//*[text()='交易資訊']")
#actions.move_to_element(element).perform()

#個股日收盤價及月平均價 
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[text()='個股日收盤價及月平均價']"))
)
new_url = element.get_attribute("href")
driver.get(new_url)


#步驟3. 選取年份 民國 112 年 01 月
element = driver.find_element(By.XPATH, "//*[name='yy']")




