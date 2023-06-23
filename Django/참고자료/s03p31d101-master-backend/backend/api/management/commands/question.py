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

class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = '../file/'



 


    def _initialize(self):
        


        sql = "insert into api_introlist (id, enterprise, start, end) values ('-1', '전체', '" + str("2020.10.25 00:00") + "', '" + str("2020.10.25 23:59") + "' )"
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()




        print("[+] Done")


    def handle(self, *args, **kwargs):
        self._initialize()
