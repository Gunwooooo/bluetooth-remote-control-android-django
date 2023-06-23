from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RawCalendarSerializer
from .models import RawCalendar
from rest_framework import status
from django.http import HttpResponse, JsonResponse
import sqlite3
import simplejson as json

@api_view(['PUT'])
def rawcalendar_modify_info(request):
    print("####################")
    print(type(request.data))
    uid=request.data['uid']
    rawStringList = request.data.getlist('rawStringList')
    rawStringList.sort()
    jsonStringList = json.dumps(rawStringList)
    # for i, v in enumerate(rawStringList):
    #     print("index : {}, value: {}".format(i,v))
    try:
        rawcalendar = RawCalendar.objects.get(uid=uid)
        rawcalendar.uid = uid
        rawcalendar.rawStringList = jsonStringList
        rawcalendar.save()
    
    except RawCalendar.DoesNotExist:
        print(jsonStringList)
        qd={"uid" : uid, "rawStringList" : jsonStringList}
        serializer = RawCalendarSerializer(data=qd)
        if serializer.is_valid():
            print("Insert Success\n")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Insert Fail(duplication)\n")
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def rawcalendar_info(request):
    uid = request.GET['uid']
    try:
        queryset = RawCalendar.objects.get(uid=uid)
        print(queryset)
        serializer = RawCalendarSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RawCalendar.DoesNotExist:
        return Response(status=status.HTTP_200_OK)