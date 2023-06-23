#-*-coding:utf-8-*-
import random
import math
from django.core.management.base import BaseCommand
import json
import pandas as pd
import os
import shutil
from api import models
import jwt, bcrypt
import sqlite3
from ...models import User
import datetime
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = '../data/'
    DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")
    PATH = '../data/question/'
    IntroList_columns = (
        "id",           # 기업 고유번호
        "enterprise",   # 기업 이름
        "start",        # 채용 시작
        "end"           # 채용 끝
    ),

    Intro_columns = (
        "id",
        "index",
        "parent_id",
        "career",
        "number",
        "department",
        "title"
    ),

    ChattingList_columns = (
        "id",
        "enter_id",
        "nane"
    ),

    Chat_columns = (
        "id",
        "enter_id",
        "name"
    )



    def _load_dataframes(self):
        print(self.DUMP_FILE)
        return pd.read_pickle(self.DUMP_FILE)

   
    def _get_store(self, dataframes):
        print("안녕하세요")
        # lists = dataframes['lists']
        # print(lists)
        print(dataframes['lists'])
        return {"lists" : dataframes['lists'], "intros" : dataframes['intros']}


    def _initialize(self):
        """
        sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        data = self._load_dataframes()          ## pkl 파일에서 값 가져오기
        print(data)
        print("data 가져오기 성공 !!! *************************************************************")
        dataframes = self._get_store(data)      ## 원하는 데이터 추출하기
        print("data 가져오기 성공 !!! *************************************************************")
        # print('[*] Initializing stores...')
        print(dataframes)

        ################################################# 기업 추가 ###############################################

        lists = dataframes["lists"]
        # print(lists)
        lists_bulk = [
            models.IntroList(
                id=lists.id,
                enterprise=lists.enterprise,
                start=datetime.strptime(lists.start, '%Y.%m.%d %H:%M'),
                end=datetime.strptime(lists.end, '%Y.%m.%d %H:%M')
            )
            for lists in lists.itertuples()
        ]
        models.IntroList.objects.bulk_create(lists_bulk)

        sql = "insert into api_introlist (id, enterprise, start, end) values ('-1', '전체', '" + str("2020-10-25 00:00:00") + "', '" + str("2022-10-25 23:59:59") + "' )"
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()


        ################################################# 자소서 목록 추가 ###############################################

        intros = dataframes['intros']

        intros_bulk = [
            models.Introduction(
                id = intros.id,
                idx = intros.index,
                parent_id = intros.parent_id,
                career = intros.career,
                number = intros.number,
                department = intros.department,
                title = intros.title
            )
            for intros in intros.itertuples()
        ]
        models.Introduction.objects.bulk_create(intros_bulk)

        ################################################# 질문 추가 ########################################################


        file_list = os.listdir(self.PATH)

        questions = []
        for i in range(len(file_list)):
            file_name = file_list[i]
            pt = self.PATH + file_name +"/"
            sub_list = os.listdir(pt)
            for j in range(len(sub_list)):
                sub_name = sub_list[j]
                url = "../data/question/" + file_name + "/" + sub_name
                f = open(url, 'rt', encoding='UTF8')
                while True:
                    line = f.readline().strip('\n')
                    questions.append({'id' : line[:-1], "sup" : file_name, "sub" : sub_name[:-4]})
                    if not line : break



        x = list({question['id'] : question for question in questions}.values())

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        for data in x :
            sql = "insert into api_interview (question, major, minor) values ('" + data['id'] + "', '" + data['sup'] + "', '" + data['sub'] + "')"
            cursor.execute(sql)
            conn.commit()

        for idx in range(7):
            today = (datetime.now() - timedelta(days=idx+1)).strftime('%Y-%m-%d')
            count = random.randrange(100)
            sql = "insert into api_daily (day, count) values ('"+ str(today) +"', " + str(count) + ")"
            cursor.execute(sql)
            conn.commit()

        sql = """insert into api_habit select 1 as id, '무의식적 말습관' as title, '`이제`, `뭐지`, `솔직히` 등의 단어는 본인도 모르게 반복적으로 쓰는 단어입니다. 과도한 사용은 면접관의 귀에 거슬릴 수 있으므로 지양해야 합니다.' as content union select 2, '자신감 부족', '`~같습니다` 와 같은 표현은 면접관들에게 자신감이 부족하다는 인상을 남길 수 있습니다. 이러한 표현을 자주 쓰는지 확인하여 고칠 필요가 있습니다.' union select 3, '비격식체 사용', '일상생활에서 격식체(`~다`)를 잘 쓰기 않기 때문에 면접장에서 비격식체를 무의식적으로 쓰는 면접자들이 많습니다. 인상이나 태도를 많이 보는 면접관들에게는 자칫 가벼워 보일 수 있는 말투이므로, 본인이 비격식체를 많이 쓰지는 않는지 미리 확인하고 고칠 필요가 있습니다.' union select 4, '부정적인 말습관', '`싫습니다`, `싫어요`, 비속어 등은 면접관들에게 부정적으로 인식될 수 있습니다. 이러한 표현은 쓰지 않도록 고칠 필요가 있습니다.'"""
        cursor.execute(sql)
        conn.commit()
        
        sql = """insert into api_word select 1 as id, 1 as hid, '이제' as word union select 2, 1, '뭐지' union select 3, 1, ' 음 ' union select 4, 1, ' 그 ' union select 5, 1, ' 아 ' union select 37, 1, ' 어 '"""
        cursor.execute(sql)
        conn.commit()

        sql = """insert into api_word select 6 as id, 2 as hid, '같습니다' as word union select 7, 2, '같아요' union select 8, 2, '인거' union select 9, 2, '일거' union select 10, 2, '모르겠습니다' 
        union select 11, 2, '몰라요' union select 12, 2, '죄송합니다' union select 13, 2, '죄송' union select 14, 2, '죄송해요' union select 15, 2, '아마도' union select 16, 2, '예상됩니다' union select 17, 2, '아마'"""
        cursor.execute(sql)
        conn.commit()
        
        sql = """insert into api_word select 18 as id, 3 as hid, '했어요' as word union select 19, 3, '했거든요' union select 20, 3, '싫거든요' union select 21, 3, '싫어요' 
        union select 22, 3, '몰라요' union select 23, 3, '죄송해요' union select 24, 3, '주세요'"""
        cursor.execute(sql)
        conn.commit()

        sql = """insert into api_word select 25 as id, 4 as hid, '싫다' as word union select 26, 4, '싫어' union select 27, 4, '안해' union select 28, 4, '싫습니다' union select 29, 4, '못해' 
        union select 30, 4, '시발' union select 31, 4, '개새끼' union select 32, 4, '좆같네' union select 33, 4, '시발' union select 34, 4, '싫거든요' union select 35, 4, '싫어요' union select 36, 4, '병신'"""
        # sql = """insert into api_word (hid, word) values
        #         (4, '싫다'), (4, '싫어'), (4, '안해'), (4, '싫습니다'), (4, '못해'), (4, '시발'), (4, '개새끼'), (4, '좆같네'), (4, '새끼'), (4, '씨발'), (4, '싫거든요'), (4, '싫어요'), (4, '병신'), (4, '서정호')"""
        cursor.execute(sql)
        conn.commit()

        print("[+] Done")


    def handle(self, *args, **kwargs):
        self._initialize()
