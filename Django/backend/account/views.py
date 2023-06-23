from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import jwt, bcrypt
from backend.settings import SECRET_KEY
from datetime import datetime, timedelta
from .serializers import UserSerializer
from .models import User
from rest_framework import status
from django.http import HttpResponse, JsonResponse
# Create your views here.

###토큰 가져오기
def token_vaild(request):
    access_token = request.headers['token']
    payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
    user = User.objects.get(uid=payload['uid'])
    return user


###로그인
##   1: 일반 회원  /  2: 보호자
@api_view(['POST'])
def user_login(request):
    print("\n##### user_login #####")
    print(request.data)

    try:
        user = User.objects.get(pk=request.data['uid'])
        if not bcrypt.checkpw(request.data['password'].encode('utf-8'), user.password.encode('utf-8')):
            print("Password Fail\n")
            return JsonResponse({'token' : "null", 'message' : "pw_fail"}, status = status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        print("Login Fail\n")
        return JsonResponse({'token' : 'NULL', 'message' : "id_fail"}, status = status.HTTP_400_BAD_REQUEST)

    token = jwt.encode({'uid' : request.data['uid'], 'exp' : datetime.utcnow() + timedelta(seconds=1800)} ,SECRET_KEY, algorithm = "HS256") # timedelta 인자 : seconds, hours, days, weeks
    token = token.decode('utf-8')
    print("     Login Success\n")
    return JsonResponse({'token' : token, 'message' : "success", 'uid' : user.uid, 'protector_check' : user.protector_check}, status = status.HTTP_200_OK)


###회원가입
@api_view(['POST'])
def user_join(request):
    print("\n##### user join #####")
    print(request.data)
    mutable = request.POST._mutable
    
    password=request.data['password'].encode('utf-8')
    password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
    password_crypt = password_crypt.decode('utf-8')

    mutable = request.POST._mutable
    request.data._mutable = True
    request.data['password'] = password_crypt
    request.data._mutable = mutable

    serializer = UserSerializer(data=request.data)
    print(serializer)

    if serializer.is_valid():
        print("Insert Success\n")
        serializer.save()
        user = User.objects.get(pk= request.data['uid'])
        print(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print("Insert Fail(duplication)\n")
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

###유저 상세 정보
@api_view(['GET'])
def user_info(request):
    user = token_vaild(request)
    print(user)
    queryset = User.objects.get(uid=user.uid)
    print(queryset)
    serializer = UserSerializer(queryset)

    return Response(serializer.data)

@api_view(['GET'])
def user_duplicate_check(request):
    print(request)
    uid = request.GET['uid']
    try:
        User.objects.get(uid=uid)
        print(User.objects.get(uid=uid))
        print("중복임")
        return Response({'duplicate' : False})
        
        
    except User.DoesNotExist:
        print("중복아님")
        return Response({'duplicate' : True})

@api_view(['GET'])
def user_protector_inquire(request):
    print(request)
    uid = request.GET['uid']
    try:
        user = User.objects.get(uid=uid, protector_check=True)
        print(User.objects.get(uid=uid))
        print("보호자 조회성공")
        return Response({'protector_name' : user.name}, status=status.HTTP_201_CREATED)
        
    except User.DoesNotExist:
        print("보호자 조회실패")
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def user_modify_info(request):
    print("####################")
    print(request)
    uid = request.data['uid']
    name = request.data['name']
    protector = request.data['protector']

    print(uid + "      " + name + "      " + protector)
    user = User.objects.get(uid=uid)
    user.name = name
    user.protector = protector
    user.save()
    print(user)
    return Response(status=status.HTTP_201_CREATED)