from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from backend.settings import SECRET_KEY
from datetime import datetime, timedelta
from .serializers import AlarmSerializer
from .models import Alarm
from rest_framework import status
from django.http import HttpResponse, JsonResponse
import sqlite3

@api_view(['PUT'])
def alarm_modify_info(request):
    print("####################")
    print(request)
    uid = request.data['uid']
    morning = request.data['morning']
    afternoon = request.data['afternoon']
    evening = request.data['evening']
    morning_switch = request.data['morning_switch']
    afternoon_switch = request.data['afternoon_switch']
    evening_switch = request.data['evening_switch']
    try:
        alarm = Alarm.objects.get(uid=uid)
        if morning_switch == "false":
            morning_switch = False
        elif morning_switch == "true":
            morning_switch = True
        if afternoon_switch == "false":
            afternoon_switch = False
        elif afternoon_switch == "true":
            afternoon_switch = True
        if evening_switch == "false":
            evening_switch = False
        elif evening_switch == "true":
            evening_switch = True
        alarm.morning = morning
        alarm.afternoon = afternoon
        alarm.evening = evening
        alarm.morning_switch = morning_switch
        alarm.afternoon_switch = afternoon_switch
        alarm.evening_switch = evening_switch
        alarm.save()
    
    except Alarm.DoesNotExist:
        serializer = AlarmSerializer(data=request.data)
        if serializer.is_valid():
            print("Insert Success\n")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Insert Fail(duplication)\n")
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)

###유저 상세 정보
@api_view(['GET'])
def alarm_info(request):
    uid = request.GET['uid']
    try:
        queryset = Alarm.objects.get(uid=uid)
        print(queryset)
        serializer = AlarmSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Alarm.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)