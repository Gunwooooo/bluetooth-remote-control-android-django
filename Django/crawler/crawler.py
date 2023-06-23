from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import json

def toJson(mnet_dict):
    with open('C:/Users/USER/AndroidStudioProjects/Android/WellinkApplication/app/src/main/assets/data.json', 'w', encoding='utf-8') as file :
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')

# driver = webdriver.Chrome('./chromedriver')
# driver.implicitly_wait(3)

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get('https://www.g-health.kr/portal/bbs/selectBoardList.do?bbsId=U00186&vType=A&menuNo=200509')

driver.implicitly_wait(3)

arr = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/section[2]/div/table/tbody/tr')
result = []
    driver.find_element_by_xpath('/html/body/div[3]/div[2]/section[2]/ul/li[{}]/a'.format(j + 4)).click()
    for i in range(1, len(arr) + 1):
        data = {}
        sleep(0.3)
        driver.find_element_by_xpath('/html/body/div[3]/div[2]/section[2]/div/table/tbody/tr[{}]/td/a'.format(i)).click()

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('body > div.site-body > div.container.sub-news > div.view-type > table > thead > tr:nth-child(1) > th')
        data['title'] = title[0].text
        date = soup.select('body > div.site-body > div.container.sub-news > div.view-type > table > thead > tr:nth-child(2) > td:nth-child(2) > span')
        data['date'] = date[0].text
        contents = soup.select('body > div.site-body > div.container.sub-news > div.view-type > table > tbody > tr > td')
        data['contents'] = contents[0].text
        result.append(data)
        sleep(0.3)
        driver.back()
toJson(result)