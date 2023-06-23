#-*-coding:utf-8-*-
import pandas as pd
# from parse import load_dataframes
from datetime import datetime
from django.core.management.base import BaseCommand
import json
import socket
import re
import os
import time
import shutil
from urllib.error import HTTPError, URLError
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException, NoSuchElementException, \
    ElementNotInteractableException
from selenium.webdriver import ActionChains
import sqlite3
from ...models import IntroList

socket.setdefaulttimeout(30)
file_path = "../data/zzzzzz.json"
driver = webdriver.Chrome("C:/chromedriver")
crawled_count = 0
list = []

class Command(BaseCommand):





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


    def _crawling(self):

        print(file_path)

        day = str(datetime.today().day)
        day1 = ''
        day2 = ''
        if len(day) == 1:
            day1 = '0'
            day2 = day
        else:
            day1 = day[0]
            day2 = day[1]
        month = str(datetime.today().month)
        month1 = month[0]
        month2 = month[1]

        url = f"https://jasoseol.com/recruit"
        print(url)
        driver.get(url)
        time.sleep(0.5)
        time.sleep(3)
        div = driver.find_elements_by_xpath('/html/body/div/div/div[3]/div/div[3]/div[2]/div/div/div/div[2]/div/div[1]')
        div2 = driver.find_elements_by_xpath('/html/body/div/div/div[3]/div/div[3]/div[2]/div/div/div/div[2]/div')
        print(len(div))
        print(len(div2))
        count = 0;
        st = 510
        for i in div:
            count +=1
            print(div2[count].get_attribute('day')[4] + " " + div2[count].get_attribute('day')[5] + " " + div2[count].get_attribute('day')[6] + " " + div2[count].get_attribute('day')[7])
            try:
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '2'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '3'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '4'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '5'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '6'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '7'):
                    continue
                if (div2[count].get_attribute('day')[4] == '1' and div2[count].get_attribute('day')[5] == '1') and (div2[count].get_attribute('day')[6] == '0' and div2[count].get_attribute('day')[7] == '8'):
                    continue
                if (div2[count].get_attribute('day')[4] == month1 and div2[count].get_attribute('day')[5] == month2) and (div2[count].get_attribute('day')[6] == day1 and div2[count].get_attribute('day')[7] == day2):
                    print("오늘날짜 입니다.")
                    break
                if i.find_element_by_xpath('div[1]').text == '끝':
                    # print('skip')
                    continue
                data = {}
                i.find_element_by_xpath('div[2]/span').click()
                time.sleep(1)
                data['index'] = st
                st +=1
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



    def _crawlingToday(self):

        d = IntroList.objects.count()-1
        print(d)
        self._crawling()

        # global list

        with open(file_path, 'w', encoding='UTF8') as outfile:
            json.dump(list, outfile, ensure_ascii=False)

        print("Crawling End")
    def handle(self, *args, **kwargs):
        self._crawlingToday()
