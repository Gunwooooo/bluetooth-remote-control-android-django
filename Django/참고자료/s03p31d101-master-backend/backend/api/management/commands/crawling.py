#-*-coding:utf-8-*-
import pandas as pd
# from parse import load_dataframes

import json
import socket
import re
import time
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
# clickAndRetrieve() 과정에서 urlretrieve 이 너무 오래 걸릴 경우를 대비해 타임 아웃 지정
socket.setdefaulttimeout(30)
file_path = "../data/data.json"
# 이미지들이 저장될 경로 및 폴더 이름
# 드라이버 경로 지정 (Microsoft Edge)
driver = webdriver.Chrome("C:/chromedriver")
# 크롤링한 이미지 수
crawled_count = 0

list = []
def click_and_retrieve(img, id):
    global crawled_count
    try:
        img.click()
        tmp = driver.find_element_by_xpath(
            '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div[1]/div[3]/div[3]/c-wiz/div/div/div/div[3]/span/div/div[1]/div[1]/a[1]/div[1]/img').get_attribute('src')
    except HTTPError:
        print("ㅡ HTTPError & 패스 ㅡ")
        pass

    except NoSuchElementException:
        print("ㅡ NoSuchElementException ㅡ")
        time.sleep(3)
        pass
    except WebDriverException:
        print("ㅡ NoSuchElementException ㅡ")
        time.sleep(3)
        pass
def crawling():
    # time.sleep(1.5)
    # image = image.replace(" ", "")
    # image = re.sub('[-=.#/?:@%^*_+/~`;<>,$&(){}]', '',image)
    # print(crawled_count)
    # print(" : " + image)
    # 이미지 고급검색 중 이미지 유형 '사진'

    url = f"https://jasoseol.com/recruit"
    driver.get(url)
    time.sleep(0.5)
    driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[3]/div[1]/div[1]/div[2]/span[1]').click()
    time.sleep(3)
    div = driver.find_elements_by_xpath('/html/body/div/div/div[3]/div/div[3]/div[2]/div/div/div/div[2]/div/div[1]')
    count = 0;
    for i in div:
        if count < 170:
            count += 1
            continue

        try:
            if i.find_element_by_xpath('div[1]').text == '끝':
                # print('skip')
                continue
            data = {}
            i.find_element_by_xpath('div[2]/span').click()
            time.sleep(1)
            data['index'] = len(list)
            enterprise = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[1]/div[1]/div/div[2]/div[1]/span').text
            data['enterprise'] = enterprise
            print(enterprise)
            start = driver.find_element_by_xpath(
                '/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/span[1]').text
            data['start'] = start

            end = driver.find_element_by_xpath(
                '/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/span[2]').text
            data['end'] = end

            department = []
            tmp = driver.find_elements_by_xpath('/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[1]/div[2]/table/tbody/tr')
            
            index = 1
            for j in tmp:
                tmpdict  = {}
                tmpdict['career'] = j.find_element_by_xpath('td[1]').text
                tmpdict['name'] = j.find_element_by_xpath('td[2]').text
                tmpdict['qid'] = index
                index += 1
                btn = j.find_element_by_xpath('td[4]/div')
                actions = webdriver.ActionChains(driver).move_to_element(btn)
                actions.perform()
                time.sleep(0.5)

                tmp2 = driver.find_elements_by_xpath(
                    '/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[3]/ul/li')
                question = []
                idx = 1
                for k in tmp2:
                    tmpdict2 = {}
                    tmpdict2["question"] = k.find_element_by_xpath('div[1]').text
                    tmpdict2['length'] = k.find_element_by_xpath('div[2]/span').text
                    question.append(tmpdict2)
                    idx +=1
                tmpdict['question'] = question
                department.append(tmpdict)

            data['department'] = department
            list.append(data)
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/img').click()
        except NoSuchElementException:
            print("ㅡ NoSuchElementException ㅡ")
            try:
                driver.find_element_by_xpath(
                    '/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/img').click()
            except NoSuchElementException:
                print("ㅡ NoSuchElementException ㅡ")
        except ElementClickInterceptedException:
            print("ㅡ ElementClickInterceptedException ㅡ")
            # driver.find_element_by_xpath(
            #     '/html/body/div/div/div[3]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/img').click()
        except ElementNotInteractableException:
            print("ㅡ ElementNotInteractableException ㅡ")
    

def main():

    # 이미 크롤링했던 검색어일 때
    #input에 name넣어서 for문 돌리기

    # query = input("입력: ")
    # dataframes = load_dataframes()
    # print(dataframes['stores']['id'])
    # stores = dataframes['stores']
    # stores = stores.loc[:, ['id', 'store_name', 'latitude', 'longitude', 'category', 'score', 'review_cnt']]
    # print(stores)

    # images = dataframes['stores']['store_name']
    # ids = dataframes['stores']['id']
    #print(dataframes['no'])
    crawling()
    #   print(images[ids[i]])
    # for i in range(10):
    global list
    # print(list)
    with open(file_path, 'w', encoding='UTF8') as outfile:
        json.dump(list, outfile, ensure_ascii=False)
    # for i in range(100):
    #     print(dataframes['store_name'][i])

    # score = dataframes[dataframes["stores"]['review_cnt'] >= 1]
    # print(score)
    # score = pd.merge(
    #     score, dataframes["reviews"], left_on="id", right_on="store"
    # )
    #
    # score = score.groupby(["store"])
    # score = score['score'].mean().reset_index()
    # print(score)
    #

    # stores = pd.merge(
    #     stores, score, left_on="id", right_on="store"
    # )
    # # stores = stores[stores['address'].str.contains('경상북도') | stores['address'].str.contains('대구광역시')]
    # # stores = stores[stores['review_cnt'] >= 1].reset_index()
    # stores = stores[stores['menu_list'] != ""]
    # stores.set_index('id', drop=True)
    #
    # print(stores)
    # print(stores.columns)
    print("crawling 끝")

if __name__ == "__main__":
    main()
