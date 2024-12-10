from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from lxml import etree

# 配置 ChromeOptions
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1440,768")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


#PS: 請限制瀏覽器 1440x768 的視窗大小來進行以下步驟 步驟1. 前往 台灣證券交易所 頁面 https://www.twse.com.tw/zh/index.html
driver.get("https://www.twse.com.tw/zh/index.html")

#交易資訊
element = driver.find_element(By.XPATH, "//*[text()='交易資訊']")

#個股日收盤價及月平均價 
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[text()='個股日收盤價及月平均價']"))
)
new_url = element.get_attribute("href")
driver.get(new_url)


#步驟3. 選取年份 民國 112 年 01 月
month_element = driver.find_element(By.XPATH, "//*[@name='yy']")
select = Select(month_element)
select.select_by_visible_text("民國 112 年")

day_element =  driver.find_element(By.XPATH, "//*[@name='mm']")
select = Select(day_element)
select.select_by_visible_text("01月")


#步驟4. 輸入股票代碼 2330
stock_element =  driver.find_element(By.XPATH, "//*[@name='stockNo']")
stock_element.clear()
stock_element.send_keys("2330")

#步驟5. 點選查詢按鈕
search_element =  driver.find_element(By.XPATH, "//button[@class='search']")
search_element.click()

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//td[text()='月平均收盤價']"))
)


#步驟6. 將台積電 112 年 01 月份的每日收盤價 print 出來
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
dom = etree.HTML(str(soup))
all_trs = dom.xpath(("//tbody//tr"))
print("台積電 112 年 01 月份的每日收盤價 ")
print("日期,      收盤價")
for tr in all_trs:
     print(f"{tr[0].text}, {tr[1].text}")



#步驟7. 截圖台積電 112 年 01 月份的每日收盤價資訊
zoom_level = 0.75
driver.execute_script(f"document.body.style.zoom='{zoom_level}'")
time.sleep(5)
target = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='月平均收盤價']"))
    )
actions = ActionChains(driver)
actions.scroll_by_amount(0, 200).perform()
driver.save_screenshot("tsmc.png")
time.sleep(20)

driver.quit()