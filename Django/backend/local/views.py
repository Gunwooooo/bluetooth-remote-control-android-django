from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.settings import SECRET_KEY
from datetime import datetime, timedelta
from .serializers import HospitalInfoSerializer, PharmacyInfoSerializer
from .models import HospitalInfo, PharmacyInfo
from rest_framework import status
from django.http import HttpResponse, JsonResponse
import sqlite3

@api_view(['GET'])
def local_hospital(request):
    print("local_hospital request : ")
    x = request.GET['x']
    y = request.GET['y']
    print(x)
    print(y)
    sql = f"select * from local_hospitalInfo where (hlng - {x}) * (hlng - {x}) + (hlat - {y}) * (hlat - {y}) <= 0.0003"
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    print("Result -----------------------------")
    columns = [column[0] for column in cursor.description]
    lists = []
    for row in list:
        lists.append(dict(zip(columns, row)))
    list = {"lists" : lists}
    return Response(list)
    
@api_view(['GET'])
def local_pharmacy(request):
    print("local_pharmacy request : ")
    x = request.GET['x']
    y = request.GET['y']
    print(x)
    print(y)
    sql = f"select * from local_pharmacyInfo where (plng - {x}) * (plng - {x}) + (plat - {y}) * (plat - {y}) <= 0.0003"
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(sql)
    list = cursor.fetchall()
    print("Result -----------------------------")
    columns = [column[0] for column in cursor.description]
    lists = []
    for row in list:
        lists.append(dict(zip(columns, row)))
    list = {"lists" : lists}
    return Response(list)
