# coding=utf8
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Board, List, Card, IntroList, MyChatting, Question, Introduction, Interview, Title, Video, Card, Daily, Habit, Word, Result, Video
import jwt, bcrypt
from .serializers import UserSerializer, IntroListSerializer, QuestionSerializer, MyChattingSerializer, IntroListSerializer, TitleSerializer, CardSerializer, ResultSerializer, VideoSerializer
from rest_framework import status
from datetime import datetime, timedelta
from backend.settings import SECRET_KEY
from konlpy.tag import Hannanum
from collections import Counter
from datetime import datetime
from konlpy.tag import Twitter
import operator

from django.http import HttpResponse, JsonResponse

import sqlite3
import requests

import time
from ast import literal_eval
import os
from django.conf import settings
import cv2

url = "https://k3d101.p.ssafy.io/ai/analyze/" # to ai analyze
thumbnailurl = "https://k3d101.p.ssafy.io/backend/media/" # thumbnail 

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

def token_vaild(request):
    # token_vaild(request)
    access_token = request.headers['token']
    payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')  
    user = User.objects.get(id=payload['id'])
    return user


#######################################################################################

@api_view(['GET'])
def resultall(request):

    print("\n########## Result All #########################################################")
    print("     request.data : ", end="")
    print(request.data)

    user = token_vaild(request)   

    print("     [GET] Result All\n")        
        
    queryset = Result.objects.filter(uid=user.id)
    serializer = ResultSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['POST', 'DELETE'])
def result(request):

    print("\n########## Result Get #########################################################")
    # print("     request.data : ", end="")
    # print(request.data)

    if request.method =='POST':

        user = token_vaild(request)   

        print("     [POST] Result POST \n")        
            
        queryset = Result.objects.get(pk = request.data['id'])
        serializer = ResultSerializer(queryset)

        res = {}
        res = serializer.data
        res['emotion'] = literal_eval(res['emotion'])
        res['emotionlist'] = literal_eval(res['emotionlist'])
        res['habitlist'] = literal_eval(res['habitlist'])
        res['list'] = literal_eval(res['list'])
        res['wordlist'] = literal_eval(res['wordlist'])

        return Response(res)

    else :

        print("     [DELETE] Result Delete\n")
        
        result = Result.objects.get(pk=request.data['id'])
        result.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#######################################################################################

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def video(request):

    user = token_vaild(request)

    print("\n########## Video #########################################################")
    # print("     request.data : ", end="")
    # print(request.data)

    if request.method =='GET':

        print("     [GET] Video Get ")        
        
        queryset = Video.objects.filter(pk=request.data['id'])
        serializer = VideoSerializer(queryset, many=True)

        return Response(serializer.data)

    elif request.method =='POST':

        print("     [POST] Video Insert ")
        request.data['uid'] = user.id

        serializer = VideoSerializer(data=request.data)              
        if serializer.is_valid():            
            serializer.save()
            print("     Insert Success\n") 
            
            videos = Video.objects.get(pk = serializer.data['id'])
            path = thumbnailurl + str(videos.video)
            temp = str(videos.video).split("/")
            cv2.imwrite("media/thumbnail/" + temp[1] + ".jpg", toFrame(path))
            videos.thumbnail = "/thumbnail/" + temp[1] + ".jpg"
            videos.save()

            request.data['id'] = serializer.data['id']
            response = analyze(request)

            return Response({"id" : response}, status=status.HTTP_201_CREATED)
        
        print("     Insert Fail(duplication)\n")
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method =='PUT':

        print("     [PUT] Video Update ")    

        videos = Video.objects.get(pk=request.data['id'])

        # 기존 video.url 삭제  
        if(videos.video):
            os.remove(os.path.join(settings.MEDIA_ROOT, videos.video.path))

        serializer = VideoSerializer(videos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("     Update Success\n")
            return Response(serializer.data)

        print("     Update Fail\n")
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    else :

        print("     [DELETE] Video Delete\n")
        
        video = Video.objects.get(pk=request.data['id'])
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

################################################################################

def toFrame(video):

    # -*- coding: utf-8 -*-
    __author__ = 'Seran'     

    # 영상의 의미지를 연속적으로 캡쳐할 수 있게 하는 class
    vidcap = cv2.VideoCapture(video)
    # vidcap = cv2.VideoCapture(video)   
    
    while(vidcap.isOpened()):
        
        ret, image = vidcap.read()

        if not ret:
            break

        vidcap.release()
        return image
        # 캡쳐된 이미지를 저장하는 함수 
        # cv2.imwrite("./data/" + str(idx) + ".jpg", image)

# @api_view(['POST'])
def analyze(request):

    start_time = time.time()

    user = token_vaild(request)

    print("\n########## backend_analyze #########################################################")
    # print("     request.data : ", end="")
    # print(request.data)

    videos = Video.objects.get(pk=request.data['id'])
    
    stt = to_stt(request.data['id']).get('stt')
    # if(len(stt) == 0):
    #     stt = " "
    wc = wordcloud(stt)
    mbti = MBTI(stt)

    time0 = time.time()
    print("     stt, mbti, wordcloud success (elapsed_time : " + str(time0 - start_time) + ")")
    
    habitlist = []
    wordlist = set()
    habits = Habit.objects.all()
    for habit in habits:
        words = Word.objects.filter(hid = habit.id)
        flag = "true"
        for word in words:
            if(stt.find(str(word.word)) != -1):
                wordlist.add(word.word)
                if(flag == "true"):
                    habitlist.append({"title" : habit.title, "content" : habit.content})
                    flag = "false"

    if(len(wordlist) == 0):
        wordlist = []

    if(len(habitlist) == 0):
        habitlist.append({"title" : "무난한 말습관", "content" : "부정적이거나 무의식적인 말습관이 거의 없이 좋은 말습관을 가지고 있습니다. 음성을 다시 들어 보면서 좀 더 자연스럽게 말하는 연습을 한다면 좋은 결과가 있을 것입니다."})

    time55 = time.time()
    print("     habit success (elapsed_time : " + str(time55 - time0) + ")")

    datas = {
        "video" : str(videos.video),
        "time" : str(videos.time),
        "count" : str(wc.get('size')),
        "list" : str(wc.get('list')),
        "title" : str(mbti.get('title')),
        "contents" : str(mbti.get('contents')),
        "habitlist" : str(habitlist),
        "wordlist" : str(wordlist),
        "stt" : str(stt),
        "uid" : str(user.id),
    }

    response = requests.post(url, data=datas)

    time1 = time.time()
    print("     ai_analyze success (elapsed_time : " + str(time1 - time0) + ")")

    #####################################################################################

    result = {}
    result = response.json()
    result['uid'] = user.id
    result['content'] = datas.get("contents")
    result['video'] = datas.get("video")
    result['time'] = datas.get("time")
    result['thumbnail'] = str(videos.thumbnail)
    result['name'] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    serializer = ResultSerializer(data=result)           
    if serializer.is_valid():
        serializer.save()
        time2 = time.time()
        print("     Vido Insert Success (elapsed_time : " + str(time2 - time1) + ")")
    else:
        time2 = time.time()
        print("     Vido Insert Fail (elapsed_time : " + str(time2 - time1) + ")\n")
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    ####################################################################################

    end_time = time.time()
    print("     analyze success (total elapsed_time : " + str(end_time - start_time) + ")\n")

    # return Response(serializer.data, status=status.HTTP_201_CREATED)
    # 방금 저장한 Result 테이블의 아이디를 쏴야함
    # return Response({"id" : serializer.data['id']}, status = status.HTTP_200_OK)
    return serializer.data['id']

####################################### 로그인 ###################################################

@api_view(['POST'])
def user_login(request):

    print("\n########## user_login ######################################################################################################################################################")
    print("     request.data : ", end="")
    print(request.data)

    try:
        user = User.objects.get(pk=request.data['id'])
        if not bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password.encode('utf-8')):
            print("     Password Fail\n")
            return JsonResponse({'token' : "null", 'message' : "pw_fail"}, status = status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        print("     Login Fail\n")
        return JsonResponse({'token' : 'NULL', 'message' : "id_fail"}, status = status.HTTP_400_BAD_REQUEST)

    token = jwt.encode({'id' : request.data['id'], 'exp' : datetime.utcnow() + timedelta(seconds=1800)} ,SECRET_KEY, algorithm = "HS256") # timedelta 인자 : seconds, hours, days, weeks
    token = token.decode('utf-8')


    day = datetime.now().strftime('%Y-%m-%d')
    print(day)
    if Daily.objects.filter(day = day).exists():
        today = Daily.objects.get(day = day)
        today.count += 1
        today.save()
        # print("값 증가")
    else:
        serializer = Daily(day = day, count = 1)
        serializer.save()
        # print("오늘 날짜 생성")

    print("     Login Success\n")

    return JsonResponse({'token' : token, 'message' : "success", 'user_id' : user.id}, status = status.HTTP_200_OK)


####################################### CRUD ###################################################

@api_view(['POST'])
def user_join(request):

    print("\n########## user_join ######################################################################################################################################################")
    print("     request.data : ", end="")
    print(request.data)

    password = request.data['password'].encode('utf-8')
    password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
    password_crypt = password_crypt.decode('utf-8')
    request.data['password'] = password_crypt

    serializer = UserSerializer(data=request.data)
    print(serializer)              
    if serializer.is_valid():
        print("     Insert Success\n")
        serializer.save()
        
        user = User.objects.get(pk = request.data['id'])
        print(user)

        #################################################### board 만들기 ####################################################
        sql = "insert into api_board (title, user_id_id) values ('자기소개서 목록', '" + str(request.data['id']) + "')"
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        #################################################### List 만들기 ####################################################
        board = Board.objects.get(user_id_id = request.data['id'])

        for i in range(1, 7):
            if i == 1:
                val = "자기소개서 작성 지원"
            elif i == 2:
                val = "서류 전형"
            elif i == 3:
                val = "1차 전형"
            elif i == 4:
                val = "2차 전형"
            elif i == 5:
                val = "3차 전형(최종 합격)"
            else:
                val = "탈락"
            pos = i*65535
            sql = "insert into api_list (title, pos, board_id_id) values ('" + str(val) + "', '" + str(pos) + "', '" + str(board.bid) + "')"
            print(sql)
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        ####################################################### 전체 채팅방 추가 ###################################################
        
        sql = "insert into api_mychatting (cid, name, uid_id) values (-1, '전체', '" + str(request.data['id']) + "')"
        cursor.execute(sql)
        conn.commit()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("     Insert Fail(duplication)\n")
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


######################################################## 유저 정보 출력 ##########################################################################
@api_view(['GET', 'PUT'])
def user_info(request):

    user = token_vaild(request)

    if request.method =='GET':
        queryset = User.objects.get(id=user.id)
        print(queryset)
        serializer = UserSerializer(queryset)

        return Response(serializer.data)
    else:
        user.name = request.data['name']
        print(request.data['major'])
        if request.data['major'] == None:
            request.data['major'] = user.major
            request.data['minor'] = user.minor

        user.major = request.data['major']
        user.minor = request.data['minor']
        user.save()

        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def profile(request):

    user = token_vaild(request)

    # 기존 user.profile 삭제  
    if(user.profile):
        os.remove(os.path.join(settings.MEDIA_ROOT, user.profile.path))

    user.profile = request.data['profile']
    user.save()

    return Response(status=status.HTTP_200_OK)



######################################################3 채팅방 추가하는 화면 #########################################################################
@api_view(['GET'])
def allChat(request):

    user = token_vaild(request)

    conn = sqlite3.connect("db.sqlite3")
    
    cursor = conn.cursor()

    sql = "select * from api_introlist where enterprise not in (select name from api_mychatting where uid_id = '" + str(user.id) + "') group by enterprise"

    cursor.execute(sql)

    chats = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    results = []
    for row in chats:
        results.append(dict(zip(columns, row)))

    return Response(results)
    

########################################  GET : 채팅 왼쪽 부분       POST : 채팅 왼쪽에 추가하기 ###############################################################
@api_view(['GET', 'POST', 'DELETE'])
def chatting(request):

    user = token_vaild(request)

    if request.method =='GET':

        queryset = MyChatting.objects.filter(uid=user.id)
        print(queryset)
        serializer = MyChattingSerializer(queryset, many=True)

        return Response(serializer.data)
    elif request.method =='POST':
        enterprise = IntroList.objects.get(id = request.data['cid'])
        sql = "insert into api_mychatting (cid, name, uid_id) values ('" + str(enterprise.id) + "', '" + str(enterprise.enterprise) + "', '" + str(user.id) + "')"

        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return Response(status=status.HTTP_201_CREATED)
    else:
        print(request.query_params.get("cid"))
        enterprise = MyChatting.objects.get(cid=request.query_params.get("cid"))
        print(enterprise)
        enterprise.delete()

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def entChat(request):

    print("****************************************************")
    print(request.data)
    print("****************************************************")
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    sql = "select * from api_chatting where chatlist_id_id = " + str(request.data['cid']) + " order by  date"
    cursor.execute(sql)

    chats = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    results = []
    for row in chats:
        results.append(dict(zip(columns, row)))

    return Response(results)


######################################################## 칸반 보드 ########################################################

@api_view(['GET'])
def board(request):

    print("\n########## Board ######################################################################################################################################################")
    print("     request.data : ", end="")
    print(request.data)

    print("     [GET] board Select All \n")

    user = token_vaild(request)
    # print(user.id)
    board = Board.objects.get(user_id_id=user.id)

    sql = "select * from api_board where bid = " + str(board.bid)

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(sql)
    
    result = cursor.fetchall()
    print(result)

    columns = [column[0] for column in cursor.description]
    results =[]
    for row in result:
        results.append(dict(zip(columns, row)))
    
    result = {}
    result = results[0]
    print(result)


    sql = "select * from api_list where board_id_id = " + str(board.bid)
    cursor = conn.cursor()
    cursor.execute(sql)
    
    list = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    lists = []
    for row in list:
        lists.append(dict(zip(columns, row)))


    for (idx, list) in enumerate(lists):
        sql = "select * from api_card where list_id_id = " + str(list['lid'])
        cursor = conn.cursor()
        cursor.execute(sql)
    
        card = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        cards = []
        for row in card:
            cards.append(dict(zip(columns, row)))
        
        card = {"cards" : cards}
        lists[idx].update(card)


    list = {"lists" : lists}

    result.update(list)
    


    return Response(result)


@api_view(['PUT', 'GET'])
def card(request):

    print("\n########## Card ######################################################################################################################################################")
    print("     request.data : ", end="")
    print(request.data)


    if request.method =='PUT':
        print("     [GET] Card Select All \n")


        sql = "update api_card set list_id_id = " + str(request.data['listId']) + ", pos = " + str(request.data['pos']) + " where cid = " + str(request.data['id'])

        print(sql)
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute(sql)
    
        conn.commit()

        return Response(status=status.HTTP_201_CREATED)

    else:
        card = Card.objects.get(cid=request.query_params.get("cid"))
        introList = IntroList.objects.get(id=card.intro_id)

        print(introList)
        print("-----------------------------------------------")

        intro_serializer = IntroListSerializer(introList, data = introList)

        intro_dict = model_to_dict( introList )
        print(intro_serializer)

        return Response(intro_dict)


######################################################## 칸반에 추가 하기(자소서 클릭 시) #################################################################################33
@api_view(['POST', 'DELETE'])
def add_card(request):

    user = token_vaild(request)
    print("\n########## add_card ######################################################################################################################################################")
    print("     request.data : ", end="")
    print(request.data)

    user = token_vaild(request)
    if request.method =='POST':
        print("     [INSERT] Card Insert\n")

        intro = IntroList.objects.get(id=request.data['id'])

        state = True
        if Card.objects.filter(user_id = user.id, intro_id=intro.id).exists():
            card = Card.objects.get(user_id = user.id, intro_id=intro.id)
            card.delete()
        else:
            board = Board.objects.get(user_id_id = user.id)
            b_list = List.objects.get(board_id_id = board.bid, pos = 65535)
            department = Introduction.objects.get(parent_id = intro.id, idx = request.data['idx'], number = 1).department
            print("---------------------------------------------------------------------------------------------")
            sql = "insert into api_card (title, start, end, pos, list_id_id, user_id, intro_id, department, idx) values ('" + str(intro.enterprise) + "', '" + str(intro.start) + "', '" + str(intro.end) +  "', '" + str(request.data['pos']) + "', '" + str(b_list.lid) + "', '" + str(user.id) + "', '" + str(intro.id) + "', '" + str(department) +"', '"+ str(request.data['idx']) +"')"

            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

    else:
        print("     [DELETE] Card Delete\n")
        card = Card.objects.get(cid=request.query_params.get("id"))
        questions = Question.objects.filter(writer = user.id, intro_id_id = card.intro_id, department = card.department)
        card.delete()
        questions.delete()

    return Response(status=status.HTTP_201_CREATED)



######################################################## 자소서 항목 출력 ##########################################################################
@api_view(['GET'])
def introduction(request):

    user = token_vaild(request)


    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    sql = "select a.id as id, a.idx as idx, enterprise, career, number, department, title from api_introduction a, api_introlist i where a.parent_id = i.id and a.parent_id = '"+ str(request.query_params.get("id")) +"'"
    cursor.execute(sql)

    chats = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    results = []
    for row in chats:
        results.append(dict(zip(columns, row)))

    state = True
    if Card.objects.filter(user_id = user.id, intro_id=request.query_params.get("id")).exists():
        state = True
    else:
        state = False
    
    result = {"results" : results, "state" : state}
    # print(results)
    print("#########################################################################################################################################")
    return Response(result)


### 얘는 숫자만 핑료함 위에 자소서 개수
@api_view(['GET'])
def my_qustion(request):

    user = token_vaild(request)
    print("#############################################################################################################")
    print(request.query_params.get("id"))
    print(request.query_params.get("department"))
    
    print("#############################################################################################################")

    if Question.objects.filter(writer = user.id, intro_id_id=request.query_params.get("id"), idx = request.query_params.get("idx")).exists():
        print("hi") 
    else:
        parent_id = request.query_params.get("id")
        idx = request.query_params.get("idx")
        cnt = Introduction.objects.filter(parent_id=parent_id, idx=idx).count()
        ## 자소서 항목 집어 넣기
        contents = ""
        intro_id = parent_id
        writer = user.id
        print(cnt)
        for i in range(cnt):
            number = i+1
            title = Introduction.objects.get(parent_id = parent_id, number = number, idx = idx).title
            department = Introduction.objects.get(parent_id = parent_id, number = number, idx = idx).department
            question = Question(number = number, title= title, contents = contents, intro_id_id = intro_id, writer = writer, department = department, idx = idx)
            question.save()
    
    print("my_question page call!!!!")
    queryset = Question.objects.filter(writer = user.id, intro_id_id=request.query_params.get("id"), idx = request.query_params.get("idx"))
    serializer = QuestionSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(['PUT', 'GET'])
def select_question(request):

    user = token_vaild(request)

    ##### 이전 자소서 항목 저장하기
    if request.method =='PUT':
        question = Question.objects.get(writer = user.id, number = request.data['number'], intro_id_id = request.data['id'], idx = request.data['idx'])
        question.contents = request.data['contents']
        question.save()

        return Response(True)

    ##### 이전 자소서 항목 가져오기
    else:
        question = Question.objects.get(writer = user.id, number = request.query_params.get("number"), intro_id_id = request.query_params.get("id"), idx = request.query_params.get("idx"))
        print(question)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)



############################################### 질문 보내주기 ######################################################################

@api_view(['GET'])
def interview(request):

    user = token_vaild(request)

    type = request.query_params.get("type")
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    if type == "1":
        sql = "select * from api_interview where major = '개인사' or major = '성장과정' order by random() limit 5";
    elif type == "2":
        if user.major == '컴퓨터':
            sql = "select * from api_interview where major = '활동' or minor = '컴퓨터' and id != 206 order by random() limit 5"
        else:
            sql = "select * from api_interview where major = '활동' or minor = '전공' order by random() limit 5"
    else:
        sql = "select * from api_interview where major = '기타' order by random() limit 5"

    cursor.execute(sql)
    
    interview = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    interviews = []
    for row in interview:
        interviews.append(dict(zip(columns, row)))


    return Response(interviews)




############################# 최근공고 / 마감공고 / 내 자소서 마감 #####################################################################
@api_view(['GET'])
def recommend(request):

    user = token_vaild(request)

    type = request.query_params.get("type")
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    if type == "1":
        sql = "select * from api_introlist order by start desc limit 5"
    elif type =="2":
        sql = "select * from api_introlist where Datetime('now') < end order by end limit 5"
    else:
        sql = "select i.id as id, enterprise, start, end from api_introlist i, api_question q where i.id = q.intro_id_id and q.writer = '"+ str(user.id) +"' group by enterprise order by end limit 5"
    
    cursor.execute(sql)
    
    introlist = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    introlists = []
    for row in introlist:
        introlists.append(dict(zip(columns, row)))


    return Response(introlists)



######################################### 첫화면 메인 자소서 등록 ##############################################################################

@api_view(['POST', 'GET', 'PUT'])
def title(request):

    user = token_vaild(request)

    to_stt("1")

    # 가장 초기에 메인 자소서 등록
    if request.method =='POST':
        serializer = Title(uid =user.id, eid = request.data['id'])
        serializer.save()
        print("메인 자소서 등록 완료")
        return Response(True)

    # 메인 자소서 관련 결과 보여주기
    ########################################## 이 부분 question이 아니라 title기준으로 바꿔야함
    elif request.method =='GET':
        if Title.objects.filter(uid = user.id).exists():
            title = Title.objects.get(uid = user.id)
            text = Question.objects.filter(writer = user.id, intro_id_id = title.eid)
            stt = []
            for i in range(len(text)):
                stt.append(text[i].contents)

            text = ""
            for i in range(len(stt)):
                text += stt[i]

            ################################# MBTI 분석 #######################################
            mbti = MBTI(text)
            ################################# 형태소 분석 #######################################
            hannanum = Hannanum()

            lists = hannanum.nouns(text)

            ret = Counter(lists)

            rank = []
            for key in ret:
                if key == "것" or key == '등' or key == '와':
                    continue
                rank.append({"name" : key, "value" : ret[key]})

            sorted_rank = sorted(rank, key=(lambda x: x['value']), reverse=True)

            size = len(sorted_rank)

            rank = sorted_rank[0:31]
            print(size)
            enterprise = IntroList.objects.get(id=title.eid).enterprise
            return Response({"list" : rank, "size" : size, "response" : True, 'enterprise' : enterprise, 'title' : mbti.get('title'), "contents" : mbti.get('contents')})
           
        else:
            return Response({'response' : False})
    # 메인 자소서 바꾸기
    else:
        serializer = Title.objects.get(uid = user.id)
        print(serializer.eid)
        serializer.eid = request.data['id']
        serializer.save()
        return Response(True)


######################### 자기 자소서 목록 / 마감 임박 목록 ########################################################
@api_view(['GET'])
def mylist(request):

    user = token_vaild(request)

    type = request.query_params.get("type")

    if type == "1":
        queryset = Card.objects.filter(user_id = user.id)
        serializer = CardSerializer(queryset, many=True)

        return Response(serializer.data)
    else:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        sql = "select * from api_card where user_id = '" + str(user.id) + "' and end > datetime('now') order by end limit 5"
    
        cursor.execute(sql)
    
        introlist = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        introlists = []
        for row in introlist:
            introlists.append(dict(zip(columns, row)))


        return Response(introlists)

################################### 일 누적자 수 계산 ##########################################################
@api_view(['GET'])
def daily(request):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    sql = "select * from api_daily order by day desc limit 7"
    
    cursor.execute(sql)
    
    daily = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    dailys = []
    for row in daily:
        dailys.append(dict(zip(columns, row)))


    return Response(dailys)
    

############################### 첫 페이지 ##############################################################################
@api_view(['GET'])
def count(request):
    
    user = token_vaild(request)

    type = request.query_params.get("type")
    
    if type == "1":
        cnt = Card.objects.filter(user_id = user.id).count()
        return Response({"count" : cnt})
    elif type == "2":
        cnt = Video.objects.filter(uid = user.id).count()
        return Response({"count" : cnt})
    else:
        return Response(True)
    





############################################################### stt로 변환 하기 #########################################################
def to_stt(idx):
    videos = Video.objects.get(id = idx)
    stt = []
    if(videos.first_sst != "등"):
        stt.append(videos.first_sst + " ")
    if(videos.second_sst != "등"):
        stt.append(videos.second_sst + " ")
    if(videos.third_sst != "등"):
        stt.append(videos.third_sst + " ")
    if(videos.fourth_sst != "등"):
        stt.append(videos.fourth_sst + " ")
    if(videos.fifth_sst != "등"):
        stt.append(videos.fifth_sst + " ")
    if(videos.sixth_sst != "등"):
        stt.append(videos.sixth_sst + " ")

    if len(stt) == 0:
        return {"stt" : "기록된 정보가 없습니다."}

    text = ""
    for i in range(len(stt)):
        text += stt[i]

    return {"stt" : text}


############################################################# wordcloud ################################################################
def wordcloud(stt):
    hannanum = Hannanum()

    lists = hannanum.nouns(stt)
    
    cnt = 0
    for list in lists:
        if list[-3:] == '입니다':
            lists[cnt] = list[:-3]
        cnt +=1
    ret = Counter(lists)

    rank = []
    # print(ret)
    for key in ret:
        if key == "것" or key == '등' or key == '와':
            continue
        rank.append({"name" : key, "value" : ret[key]})

    sorted_rank = sorted(rank, key=(lambda x: x['value']), reverse=True)

    size = len(sorted_rank)

    rank = sorted_rank[0:31]
    
    # print(rank)
    # print(size)

    return {"list" : rank, "size" : size}





################################################################# MBTI ############################################################
def MBTI(stt):
    dic = {'E': ['책임감', '관리', '해결', '팀원', '열정', '역량', '참여', '직접', '활동', '정열', '외부', '사람', '행동', '모임', '공동체', '공적', '말', '도시', '토론', '외향성', '대인관계', '유지', '사교', '자기', '집중', '적극성', '말로', '경험', '다음', '이해', '스스로','적극', '도전',],
           'I': ['생각', '이해', '경험', '집중', '장소', '도서관', '개인', '사적', '숲', '내향성', '깊이', '대인관계', '유지', '자기', '내부', '부활동', '신중', '글', '서서히'],
           'S': ['실제', '나무', '사실', '감각', '경험', '지금', '현재', '초점', '정확', '처리', '관찰', '생산', '보존', '거북이', '오감', '의존', '중시', '사건', '묘사', '경향', '추수', '함'],
           'N': ['가능성', '숲', '미래', '신속', '처리', '상상력', '이론', '디자인', '통찰', '변화', '토끼', '직관', '육감', '영감', '의존', '지향', '의미', '추구', '초점', '아이디어', '비유', '암시', '묘사', '경향'],
           'T': ['진실', '논리', '분석', '사실', '관심', '정의', '머리', '관성', '질서', '공평', '사고', '객관', '판단', '원리', '원칙', '규범', '기준', '중시', '지적', '논평', '신뢰'],
           'F': ['팀원', '긍정', '관계', '관심', '상황', '의미', '자비', '가슴', '열정', '재치', '조화', '가치', '친절', '중심', '감정', '사람과', '정상', '참작', '설명', '사람', '영향', '포괄', '나', '우호', '협조', '친구', '배려', '도움', '사랑'],
           'J': ['개발', '프로젝트', '기획', '준비', '설계', '계획', '조직', '방향', '과단성', '집중', '일', '지배인', '결과', '판단', '목적', '목표', '기한', '엄수', '사전', '체계', '정리', '정돈', '의지', '추진', '결론', '통제', '조정', '목적의식', '감각', '기준', '자기', '의사', '신뢰'],
           'P': ['의견', '융통', '과정', '목적', '방향', '변화', '상황', '개방', '자유', '호기심', '즉흥', '질문', '놀이', '기업가', '시작', '인식', '일정', '자율', '융통성', '이해', '수용', '적응', '재량', '처리']}

    dic_sum ={  'ENFJ': ['사람', '생각', '의견', '외교', '충성', '경향', '적극', '책임감', '사교성', '사교', '참을성', '관심', '동선', '대체로', '동의', '현재', '미래', '가능성', '추구', '능란', '계획', '제시', '집단', '능력', '교직', '성직', '심리', '상담', '치료', '예술', '문학', '판매', '맹목', '대해', '자기', '이상', '개인', '언어', '표현', '성적', '열정', '염려', '지적', '마음'],
                'ENFP': ['일', '열성', '재능', '창의', '관심', '사람', '통찰', '정열', '활기', '상상력', '정적', '항상', '가능성', '시도', '문제해결', '수행', '능력', '도움', '상담', '교육', '과학', '저널리스트', '광고', '판매', '성직', '작가', '분야', '반복', '일상', '창의력', '요구', '흥미', '호기심', '성적', '재주', '자발', '표현', '독립', '우호', '열정', '상상', '활동'],
                'ENTJ': ['계획', '감정', '통솔력', '결정', '관심', '논리', '필요', '자신', '열성', '단호', '지도력', '활동', '장기', '안목', '선호', '지식', '욕구', '지적', '자극', '아이디어', '처리', '준비', '분석', '조직', '체계', '추진', '의견', '귀', '타인', '느낌', '인정', '판단', '결론', '피해', '누적', '크게', '폭발', '가능성', '전략', '비판', '조절', '도전', '직선', '객관', '이론'],
                'ENTP': ['일', '문제', '능력', '독창', '안목', '다방면', '관심', '재능', '도전', '분석', '이론', '창의력', '상상력', '시도', '솔선', '논리', '해결', '사람', '동향', '대해', '일상', '세부', '경시', '즉', '흥미', '수행', '가지', '발명가', '과학자', '해결사', '저널리스트', '마케팅', '컴퓨터', '등', '때', '경쟁', '현실', '더', '편이', '진취', '독립', '전략', '창의', '융통성', '자원'],
                'ESFJ': ['사람', '이야기', '요구', '마음', '양심', '관심', '협력', '동료', '능동', '구성원', '정리정돈', '참을성', '행동', '교직', '성직', '판매', '필요', '간호', '의료', '일이', '대한', '문제', '입장', '반대', '의견', '자신', '거절', '상처', '충성', '사교', '개인', '협동', '재치', '감동', '전통', '동정'],
                'ESFP': ['사교', '수용', '낙천', '실제', '사람', '일', '상식', '분야', '활동', '현실', '상황', '주위', '관심', '사물', '사실', '물질', '소유', '운동', '실생활', '능력', '필요', '의료', '판매', '교통', '유흥', '간호', '비서', '사무직', '감독', '기계', '수다', '깊이', '마무리', '경향', '조직체', '공동체', '분위기', '조성', '역할', '성적', '융통성', '우호', '표현', '협동', '관용', '개방'],
                'ESTJ': ['현실', '조직', '일', '능력', '분야', '사실', '지도력', '행정', '체계', '결정', '경향', '구체', '활동', '실질', '감각', '계획', '추진', '기계', '재능', '업체', '조직체', '지도자', '목표', '설정', '지시', '이행', '결과', '사업가', '관리', '생산', '건축', '발휘', '속단', '속결', '업무', '사람', '인간', '중심', '가치', '타인', '감정', '고려', '미래', '가능성', '현재', '추구', '실용', '논리', '효율', '객관', '실제', '구조', '인적'],
                'ESTP': ['현실', '사실', '개방', '일', '별로', '문제해결', '적응력', '관용', '사람', '선입관', '감각', '협책', '모색', '문제', '해결', '능력', '적응', '친구', '설명', '운동', '음식', '활동', '주로', '보고', '생활', '순발력', '기억', '예술', '멋', '판단력', '연장', '재료', '논리', '분석', '처리', '추상', '아이디어', '개념', '대해', '흥미', '행동', '지향', '융통성', '재미', '재주', '열정', '낙천', '자발', '실용', '설득'],
                'INFJ': ['분야', '직관', '통찰', '열정', '인내심', '양심', '화합', '추구', '창의력', '말', '타인', '영향력', '독창', '성과', '내적', '독립심', '신념', '자신', '영감', '구현', '정신', '지도자', '사람', '중심', '가치', '중시', '성직', '심리학', '심리치료', '상담', '예술', '문학', '테크니컬', '순수과학', '연구', '개발', '시도', '대한', '열성', '경향', '목적', '달성', '주변', '조건', '경시', '갈등', '내적인', '생활', '소유', '내면', '반응', '남', '공유', '헌신', '창의', '깊이', '결심', '개념', '전체', '이상'],
                'INFP': ['자신', '경향', '정열', '신념', '이상', '일', '인간', '능력', '헌신', '목적', '낭만', '내적', '마음', '관계', '일이', '사람', '책임감', '지향', '남', '지배', '인상', '거의', '완벽', '주의', '노동', '대가', '흥미', '자하', '이해', '복지', '기여', '언어', '문학', '상담', '심리학', '과학', '예술', '분야', '발휘', '현실', '실제', '상황', '고려', '융통성', '모험심', '창의', '깊이', '과묵', '공감'],
                'INTJ': ['독창', '타인', '사고', '비판', '분석', '직관', '자신', '목적', '능력', '노력', '분야', '창의력', '내적', '신념', '행동', '영감', '실현', '의지', '결단', '인내심', '중요시', '달성', '시간', '일', '통찰', '활용', '과학', '엔지니어링', '발명', '정치', '철학', '발휘', '일과', '사람', '그대로', '사실', '감정', '고려', '관점', '독립', '논리', '체계', '마음', '전이', '이론', '기준', '객관', '전체'],
                'INTP': ['논리', '지적', '과묵', '분석', '관심', '호기심', '추상', '문제', '해결', '하나', '대해', '말', '이해', '직관', '통찰', '재능', '개인', '인관', '관계', '친목', '잡담', '객관', '비평', '발휘', '순수과학', '연구', '수학', '엔지니어링', '개념', '경제', '철학', '심리학', '학문', '비현실적', '사교성', '결여', '경향', '자신', '능력', '은근', '과시', '때문', '회의', '초연', '이론', '독립', '사색', '독창', '자율', '자기', '결정'],
                'ISFJ': ['헌신', '자신', '타인', '책임감', '처리', '조직', '정적', '인내력', '다른', '사람', '사정', '고려', '감정', '현실', '감각', '실제', '경험', '통해', '인정', '난관', '밀고', '의존', '독창', '요구', '표현', '관심', '관찰', '분야', '의료', '간호', '교직', '사무직', '사회사업', '일', '대처', '행동', '분별', '상세', '전통', '참을성', '봉사', '보호', '매우', '동정'],
                'ISFP': ['말', '적응력', '관용', '자신', '의견', '타인', '융통성', '연기력', '속마음', '상대방', '동정', '자기', '능력', '성격', '유형', '가장', '가치', '강요', '충돌', '피하', '중시', '인간', '관계', '일', '감정', '결정', '추진', '일상', '활동', '개방', '협동', '충성', '신뢰', '자발', '이해'],
                'ISTJ': ['조직', '집중', '분별', '실제', '사실', '체계', '일', '발휘', '기억', '처리', '책임감', '현실', '감각', '보수', '경향', '문제', '해결', '과거', '경험', '적용', '반복', '일상', '대한', '인내력', '자신', '타인', '감정', '기분', '배려', '전체', '타협', '방안', '고려', '노력', '정확성', '선호', '회계', '법률', '생산', '건축', '의료', '사무직', '관리직', '능력', '위기', '상황', '안정', '신뢰', '확고', '부동', '의무'],
                'ISTP': ['상황', '능력', '객관', '사실', '인생', '관찰', '파악', '도구', '형', '이상', '발휘', '조직', '기계', '과묵', '절제', '호기심', '민감', '성과', '말', '필요', '자신', '일과', '관계', '인간관계', '직접', '가을', '에너지', '소비', '사람', '자료', '정리', '인과관계', '원리', '관심', '연장', '재능', '법률', '경제', '마케팅', '판매', '통계', '분야', '느낌', '감정', '타인', '대한', '마음', '표현', '편의', '실제', '실적', '응용', '독립', '모험', '융통성', '자기', '결정']}

    bow = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    bow_sum = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
# ########################################################################################################################
# 1. 읽어 온 resume을 분석해 mbti 값과 mbti 값에서 유도된 성향점수 반영 후 저장
# 2. resume DB 에 mbti DATA 저장할 수 있도록 DB 수정 후 MBTI DATA 반영
# # ########################################################################################################################

    text = stt

 
    spliter = Twitter()
    token = spliter.nouns(text)

    for key in dic.keys():
        for voca in token:
            if voca in dic[key]:
                bow[key] += 1
        bow[key] = bow[key]/len(dic[key])

    for key in dic_sum.keys():
        for voca in token:
            if voca in dic_sum[key]:
                for i in range(0, 4):
                    bow_sum[key[i:i+1]] += 1
        for i in range(0, 4):
            bow_sum[key[i:i+1]] = bow_sum[key[i:i+1]]/len(dic_sum[key])


    mbti_sum = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

    for key in mbti_sum.keys():
        mbti_sum[key] = bow[key] + bow_sum[key]

    mbti_type = list(mbti_sum.keys())
    mbti_reverse_type = {'E': 'I', 'S': 'N', 'T': 'F', 'J': 'P',
                         'I': 'E', 'N': 'S', 'F': 'T', 'P': 'J'}
    mbti_type_loc = {'E': 0, 'S': 1, 'T': 2, 'J': 3,
                     'I': 0, 'N': 1, 'F': 2, 'P': 3}

    mbti_best_type = {}
    mbti_worst_type = {}

    for i in range(0, 4):
        key = mbti_type[2*i] if mbti_sum[mbti_type[2*i]] > mbti_sum[mbti_type[2*i + 1]] else mbti_type[2*i + 1]
        tmp = {key: abs(mbti_sum[mbti_type[2*i]] - mbti_sum[mbti_type[2*i + 1]])}
        # print(tmp)
        mbti_best_type.update(tmp)
        tmp.clear()

        tmp = {mbti_reverse_type[key]: abs(mbti_sum[mbti_type[2*i]] - mbti_sum[mbti_type[2*i + 1]])}
        # print(tmp)
        mbti_worst_type.update(tmp)
        tmp.clear()
    # print("Score Of MBTI and Resume")
    # print(bow)
    # print("\nScore Of Only MBTI")
    # print(bow_sum)
    # print("\nSum Of Every Score")
    # print(mbti_sum)
    # print("\nDifference of Conflicted MBTI Score")
    # print(mbti_best_type)
    # print(mbti_worst_type)
    # print("")

    my_org_type = list(mbti_best_type.keys())
    my_worst_type = "".join(list(mbti_worst_type.keys()))
    # print("my_org_type :" + "".join(my_org_type) + "\n")

    my_type_sorted = sorted(mbti_best_type.items(), key=operator.itemgetter(1))
    # print("In Order by Difference of Conflicted MBTI Score")
    # print(my_type_sorted)
    # print("")
    # print("The Most Similar Type : " + my_type_sorted[0][0] + "\nThe Second Similar Type : " + my_type_sorted[1][0])
    # print("")

    my_1st_type = "".join(my_org_type)

    my_org_type[mbti_type_loc[my_type_sorted[0][0]]] = mbti_reverse_type[my_type_sorted[0][0]]
    my_2nd_type = "".join(my_org_type)
    my_org_type[mbti_type_loc[my_type_sorted[0][0]]] = mbti_reverse_type[my_org_type[mbti_type_loc[my_type_sorted[0][0]]]]

    my_org_type[mbti_type_loc[my_type_sorted[1][0]]] = mbti_reverse_type[my_type_sorted[1][0]]
    my_3rd_type = "".join(my_org_type)

    # print("my_1st_type :" + my_1st_type)
    if my_1st_type == "INTJ":
        mbti1 = "용의주도한 전략가(INTJ)"
        mbti2 = "윗자리에 있는 사람은 고독한 법, 전략적 사고에 뛰어나며 매우 극소수인 건축가형 사람은 이를 누구보다 뼈저리게 이해합니다. 전체 인구의 2%에 해당하는 이들은 유독 여성에게서는 더욱 찾아보기 힘든 유형으로, 인구의 단 0.8%를 차지합니다. 체스를 두는 듯한 정확하고 계산된 움직임과 풍부한 지식을 소유하고 있는 이들은 그들과 견줄 만한 비슷한 부류의 사람을 찾는 데 종종 어려움을 겪습니다. 건축가형 사람은 상상력이 풍부하면서도 결단력이 있으며, " + "야망이 있지만 대외적으로 표현하지 않으며, 놀랄 만큼 호기심이 많지만 쓸데없는 데 에너지를 낭비하는 법이 없습니다."
    elif my_1st_type == "INTP":
        mbti1 = "논리적인 사색가(INTP)"
        mbti2 = "사색가형은 전체 인구의 3% 정도를 차지하는 꽤 흔치 않은 성격 유형으로, 이는 그들 자신도 매우 반기는 일입니다. 왜냐하면, 사색가형 사람보다 '평범함'을 거부하는 이들이 또 없기 때문입니다. 이 유형의 사람은 그들이 가진 독창성과 창의력, 그리고 그들만의 독특한 관점과 왕성한 지적 호기심에 나름의 자부심을 가지고 있습니다. 보통 철학자나 사색가, 혹은 몽상에 빠진 천재 교수로도 많이 알려진 이들은 역사적으로 수많은 과학적 발전을 이끌어 내기도 하였습니다."
    elif my_1st_type == "ENTJ":
        mbti1 = "대담한 통솔자(ENTJ)"
        mbti2 = "통솔자형 사람은 천성적으로 타고난 리더입니다. 이 유형에 속하는 사람은 넘치는 카리스마와 자신감으로 공통의 목표 실현을 위해 다른 이들을 이끌고 진두지휘합니다. 예민한 성격의 사회운동가형 사람과 달리 이들은 진취적인 생각과 결정력, 그리고 냉철한 판단력으로 그들이 세운 목표 달성을 위해 가끔은 무모하리만치 이성적 사고를 하는 것이 특징입니다. 이들이 인구의 단 3%에 지나지 않는 것이 어쩌면 다행일 수도 있습니다. 그렇지 않으면 인구 대다수를 차지하는 소심하고 섬세한 성향의 사람들이 모두 주눅 들어 살지도 모르니까요. 단, 평소 잊고 살기는 하나 우리 삶을 윤택하게 해주는 위대한 사업가나 기관을 이끄는 통솔자형 사람들이 있음에 다행이기도 합니다."
    elif my_1st_type == "ENTP":
        mbti1 = "뜨거운 논쟁을 즐기는 변론가(ENTP)"
        mbti2 = "변론가형 사람은 타인이 믿는 이념이나 논쟁에 반향을 일으킴으로써 군중을 선동하는 일명 선의의 비판자입니다. 결단력 있는 성격 유형이 논쟁 안에 깊이 내재한 숨은 의미나 상대의 전략적 목표를 꼬집기 위해 논쟁을 벌인다고 한다면, 변론가형 사람은 단순히 재미를 이유로 비판을 일삼습니다. 아마도 이들보다 논쟁이나 정신적 고문을 즐기는 성격 유형은 없을 것입니다. 이는 천부적으로 재치 있는 입담과 풍부한 지식을 통해 논쟁의 중심에 있는 사안과 관련한 그들의 이념을 증명해 보일 수 있기 때문입니다."
    elif my_1st_type == "INFJ":
        mbti1 = "선의의 옹호자(INFJ)"
        mbti2 = "선의의 옹호자형은 가장 흔치 않은 성격 유형으로 인구의 채 1%도 되지 않습니다. 그럼에도 불구하고 나름의 고유 성향으로 세상에서 그들만의 입지를 확고히 다집니다. 이들 안에는 깊이 내재한 이상향이나 도덕적 관념이 자리하고 있는데, 다른 외교형 사람과 다른 점은 이들은 단호함과 결단력이 있다는 것입니다. 바라는 이상향을 꿈꾸는데 절대 게으름 피우는 법이 없으며, 목적을 달성하고 지속적으로 긍정적인 영향을 미치고자 구체적으로 계획을 세워 이행해 나갑니다."
    elif my_1st_type == "INFP":
        mbti1 = "열정적인 중재자(INFP)"
        mbti2 = "중재자형 사람은 최악의 상황이나 악한 사람에게서도 좋은 면만을 바라보며 긍정적이고 더 나은 상황을 만들고자 노력하는 진정한 이상주의자입니다. 간혹 침착하고 내성적이며 심지어는 수줍음이 많은 사람처럼 비추어지기도 하지만, 이들 안에는 불만 지피면 활활 타오를 수 있는 열정의 불꽃이 숨어있습니다. 인구의 대략 4%를 차지하는 이들은 간혹 사람들의 오해를 사기도 하지만, 일단 마음이 맞는 사람을 만나면 이들 안에 내재한 충만한 즐거움과 넘치는 영감을 경험할 수 있을 것입니다."
    elif my_1st_type == "ENFJ":
        mbti1 = "정의로운 사회운동가(ENFJ)"
        mbti2 = "사회운동가형 사람은 카리스마와 충만한 열정을 지닌 타고난 리더형입니다. 인구의 대략 2%가 이 유형에 속하며, 정치가나 코치 혹은 교사와 같은 직군에서 흔히 볼 수 있습니다. 이들은 다른 이들로 하여금 그들의 꿈을 이루며, 선한 일을 통하여 세상에 빛과 소금이 될 수 있도록 사람들을 독려합니다. 또한, 자신뿐 아니라 더 나아가 살기 좋은 공동체를 만들기 위해 사람들을 동참시키고 이끄는 데에서 큰 자부심과 행복을 느낍니다."
    elif my_1st_type == "ENFP":
        mbti1 = "재기발랄한 활동가(ENFP)"
        mbti2 = "활동가형 사람은 자유로운 사고의 소유자입니다. 종종 분위기 메이커 역할을 하기도 하는 이들은 단순한 인생의 즐거움이나 그때그때 상황에서 주는 일시적인 만족이 아닌 타인과 사회적, 정서적으로 깊은 유대 관계를 맺음으로써 행복을 느낍니다. 매력적이며 독립적인 성격으로 활발하면서도 인정이 많은 이들은 인구의 대략 7%에 속하며, 어느 모임을 가든 어렵지 않게 만날 수 있습니다."
    elif my_1st_type == "ISTJ":
        mbti1 = "청렴결백한 논리주의자(ISTJ)"
        mbti2 = "논리주의자형은 가장 다수의 사람이 속하는 성격 유형으로 인구의 대략 13%를 차지합니다. 청렴결백하면서도 실용적인 논리력과 헌신적으로 임무를 수행하는 성격으로 묘사되기도 하는 이들은, 가정 내에서뿐 아니라 법률 회사나 법 규제 기관 혹은 군대와 같이 전통이나 질서를 중시하는 조직에서 핵심 구성원 역할을 합니다. 이 유형의 사람은 자신이 맡은 바 책임을 다하며 그들이 하는 일에 큰 자부심을 가지고 있습니다. 또한, 목표를 달성하기 위해 시간과 에너지를 허투루 쓰지 않으며, 이에 필요한 업무를 정확하고 신중하게 처리합니다."
    elif my_1st_type == "ISFJ":
        mbti1 = "용감한 수호자(ISFJ)"
        mbti2 = "수호자형 사람은 꽤 독특한 특징을 가지고 있는데, 이 유형에 속하는 사람은 이들을 정의하는 성격 특성에 꼭 들어맞지 않는다는 점입니다. 타인을 향한 연민이나 동정심이 있으면서도 가족이나 친구를 보호해야 할 때는 가차 없는 모습을 보이기도 합니다. 조용하고 내성적인 반면 관계술에 뛰어나 인간관계를 잘 만들어갑니다. 안정적인 삶을 지향하지만 이들이 이해받고 존경받는다고 생각되는 한에서는 변화를 잘 수용합니다. 이처럼 수호자형 사람은 한마디로 정의 내리기 힘든 다양한 성향을 내포하고 있는데, 이는 오히려 그들의 장점을 승화시켜 그들 자신을 더욱 돋보이게 합니다."
    elif my_1st_type == "ESTJ":
        mbti1 = "엄격한 관리자(ESTJ)"
        mbti2 = "관리자형 사람은 그들 생각에 반추하여 무엇이 옳고 그른지를 따져 사회나 가족을 하나로 단결시키기 위해 사회적으로 받아들여지는 통념이나 전통 등 필요한 질서를 정립하는 데 이바지하는 대표적인 유형입니다. 정직하고 헌신적이며 위풍당당한 이들은 비록 험난한 가시밭길이라도 조언을 통하여 그들이 옳다고 생각하는 길로 사람들을 인도합니다. 군중을 단결시키는 데에 일가견이 있기도 한 이들은 종종 사회에서 지역사회조직가와 같은 임무를 수행하며, 지역 사회 발전을 위한 축제나 행사에서부터 가족이나 사회를 하나로 결집하기 위한 사회 운동을 펼치는 데 사람들을 모으는 역할을 하기도 합니다."
    elif my_1st_type == "ESFJ":
        mbti1 = "사교적인 외교관(ESFJ)"
        mbti2 = "사교형 사람을 한마디로 정의 내리기는 어렵지만, 간단히 표현하자면 이들은 '인기쟁이'입니다. 인구의 대략 12%를 차지하는 꽤 보편적인 성격 유형으로, 이를 미루어 보면 왜 이 유형의 사람이 인기가 많은지 이해가 갑니다. 종종 고등학교에서 치어리더나 풋볼의 쿼터백으로 활동하기도 하는 이들은 분위기를 좌지우지하며 여러 사람의 스포트라이트를 받거나 학교에 승리와 명예를 불러오도록 팀을 이끄는 역할을 하기도 합니다. 이들은 또한 훗날 다양한 사교 모임이나 어울림을 통해 주위 사람들에게 끊임없는 관심과 애정을 보임으로써 다른 이들을 행복하고 즐겁게 해주고자 노력합니다."
    elif my_1st_type == "ISTP":
        mbti1 = "만능 재주꾼(ISTP)"
        mbti2 = "냉철한 이성주의적 성향과 왕성한 호기심을 가진 만능재주꾼형 사람은 직접 손으로 만지고 눈으로 보면서 주변 세상을 탐색하는 것을 좋아합니다. 무엇을 만드는 데 타고난 재능을 가진 이들은 하나가 완성되면 또 다른 과제로 옮겨 다니는 등 실생활에 유용하면서도 자질구레한 것들을 취미 삼아 만드는 것을 좋아하는데, 그러면서 새로운 기술을 하나하나 터득해 나갑니다. 종종 기술자나 엔지니어이기도 한 이들에게 있어 소매를 걷어붙이고 작업에 뛰어들어 직접 분해하고 조립할 때보다 세상에 즐거운 일이 또 없을 것입니다. 전보다 조금은 더 향상된 모습으로요."
    elif my_1st_type == "ISFP":
        mbti1 = "호기심 많은 예술가(ISFP)"
        mbti2 = "모험가형 사람은 일반적으로 사람들이 생각하듯 야외에서 앙증맞은 나무 그림을 그리고 있는 그런 유형의 예술가는 아니지만, 진정한 예술가라고 할 수 있습니다. 실상 상당수 많은 이들이 그러한 능력을 충분히 갖추고 있기도 합니다. 이들은 그들의 심미안이나 디자인 감각, 심지어는 그들의 선택이나 행위를 통하여 사회적 관습이라는 한계를 뛰어넘고자 합니다. 실험적인 아름다움이나 행위를 통해 전통적으로 기대되는 행동양식이나 관습에 도전장을 내미는 이들은 '저를 가두어두려 하지 마세요!'라고 수없이 외칩니다."
    elif my_1st_type == "ESTP":
        mbti1 = "모험을 즐기는 사업가(ESTP)"
        mbti2 = "주변에 지대한 영향을 주는 사업가형 사람은 여러 사람이 모인 행사에서 이 자리 저 자리 휙휙 옮겨 다니는 무리 중에서 어렵지 않게 찾아볼 수 있습니다. 직설적이면서도 친근한 농담으로 주변 사람을 웃게 만드는 이들은 주변의 이목을 끄는 것을 좋아합니다. 만일 관객 중 무대에 올라올 사람을 호명하는 경우, 이들은 제일 먼저 자발적으로 손을 들거나 아니면 쑥스러워하는 친구를 대신하여 망설임 없이 무대에 올라서기도 합니다. 국제사회 이슈나 이와 관련한 복잡하고 난해한 이론과 관련한 담화는 이들의 관심을 오래 붙잡아 두지 못합니다. 사업가형 사람은 넘치는 에너지와 어느 정도의 지식으로 대화에 무리 없이 참여하기는 하나, 이들이 더 역점을 두는 것은 앉아서 말로만 하는 논의가 아닌 직접 나가 몸으로 부딪히는 것입니다."
    elif my_1st_type == "ESFP":
        mbti1 = "자유로운 영혼의 연예인(ESFP)"
        mbti2 = "갑자기 흥얼거리며 즉흥적으로 춤을 추기 시작하는 누군가가 있다면 이는 연예인형의 사람일 가능성이 큽니다. 이들은 순간의 흥분되는 감정이나 상황에 쉽게 빠져들며, 주위 사람들 역시 그런 느낌을 만끽하기를 원합니다. 다른 이들을 위로하고 용기를 북돋아 주는 데 이들보다 더 많은 시간과 에너지를 소비하는 사람 없을 겁니다. 더욱이나 다른 유형의 사람과는 비교도 안 될 만큼 거부할 수 없는 매력으로 말이죠. 천부적으로 스타성 기질을 타고난 이들은 그들에게 쏟아지는 스포트라이트를 즐기며 어디를 가나 모든 곳이 이들에게는 무대입니다. 사실상 많은 배우가 이 성격 유형에 속하기도 합니다.매우 사교적인 성향의 이들은 단순한 것을 좋아하며, 좋은 사람들과 어울려 즐거운 시간을 갖는 것보다 세상에 더 큰 즐거움은 없다고 여깁니다."


    return {"title" : mbti1, "contents" : mbti2}
