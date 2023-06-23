from django.db import models
import os
from django.conf import settings
from pytz import timezone   # 한국시간 넣기

## 유저
class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    profile = models.ImageField(upload_to='profile/', blank=True, null=True)
    major = models.CharField(max_length=20)
    minor = models.CharField(max_length=20)
    
    def __str__(self):
        return f'id : {self.id} password: {self.password} name: {self.name} major: {self.major} minor: {self.minor}'

    def delete(self, *args, **kargs):
        if self.profile:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.profile.path))
        super(User, self).delete(*args, **kargs)

############################################## 자기소개서 ####################################################

## 기업 리스트
class IntroList(models.Model):
    id = models.AutoField(primary_key=True)
    enterprise = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return f'id : {self.id} enterprise : {self.enterprise} start : {self.start} end : {self.end}'

## 자소서 질문
class Introduction(models.Model):
    id = models.AutoField(primary_key=True)
    idx = models.IntegerField()
    parent_id = models.IntegerField()
    career = models.CharField(max_length=20)
    number = models.IntegerField()
    department = models.CharField(max_length=20)
    title = models.CharField(max_length=20)

    def __str__(self):
        return f'parent_id : {self.parent_id} career : {self.career} number : {self.number} department : {self.department} title : {self.title}'

## 내 자소서 대답
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    title = models.CharField(max_length=20)
    contents = models.CharField(max_length=500)
    intro_id = models.ForeignKey(IntroList, on_delete=models.CASCADE)
    writer = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    idx = models.IntegerField()

    def __str__(self):
        return f'number : {self.number}. title: {self.title} contents: {self.contents} writer: {self.writer}, intro_id : {self.intro_id}'

############################################## 전공 면접 질문 ####################################################

## 면접 질문
class Interview(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length = 20)
    major = models.CharField(max_length = 20)
    minor = models.CharField(max_length=20)

    def __str__(self):
        return f'id : {self.id} question : {self.question} major : {self.major}, minor : {self.minor}'

############################################## 자기소개서 칸반보드 ####################################################

## 칸반 Board
class Board(models.Model):
    bid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'bid : {self.bid} user_id : {self.user_id_id} title : {self.title}'

    
## 칸반 List
class List(models.Model):
    lid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    pos = models.IntegerField()
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return f'lid : {self.lid} title = {self.title} pos = {self.pos}'

## 칸반 Card
class Card(models.Model):
    cid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    pos = models.IntegerField()
    list_id = models.ForeignKey(List, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=20)
    intro_id = models.IntegerField()
    department = models.CharField(max_length=50, null=True)
    idx = models.IntegerField()

    def __str__(self):
        return f'cid : {self.cid} title = {self.title} pos = {self.pos}'



############################################## 기업별 채팅방 ####################################################

# ## 전체 채팅 리스트 (기업과 비슷해서 추후 삭제 할 수도)
# class ChattingList(models.Model):
#     id = models.AutoField(primary_key=True)
#     enter_id = models.ForeignKey(IntroList, on_delete=models.CASCADE)
#     name = models.CharField(max_length = 20)
    

#     def __str__(self):
#         return f'name : {self.name}'

## 채팅 하나하나
class Chatting(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.CharField(max_length=20)
    contents = models.CharField(max_length=500)
    chatlist_id = models.ForeignKey(IntroList, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    date = models.DateField(null = True, blank=True)

    def __str__(self):
        return f'enterprise: {self.name}. writer: {self.writer} contents: {self.contents} date: {self.date}'


## 개인 소속 채팅 방 목록 정도
class MyChatting(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    cid = models.IntegerField()
    name = models.CharField(max_length=20)


    def __str__(self):
        return f'id : {self.id} uid : {self.uid} cid : {self.cid} name : {self.name}'

############################################## 면접영상 내용 추후 구현 ####################################################

## 면접 영상
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    video = models.FileField(upload_to='video/', blank=True, null=True)
    time = models.IntegerField(null=True)
    first_iid = models.IntegerField(null=True)
    second_iid = models.IntegerField(null=True)
    third_iid = models.IntegerField(null=True)
    fourth_iid = models.IntegerField(null=True)
    fifth_iid = models.IntegerField(null=True)
    sixth_iid = models.IntegerField(null=True)
    first_sst = models.CharField(max_length=1000, null=True)
    second_sst = models.CharField(max_length=1000, null=True)
    third_sst = models.CharField(max_length=1000, null=True)
    fourth_sst = models.CharField(max_length=1000, null=True)
    fifth_sst = models.CharField(max_length=1000, null=True)
    sixth_sst = models.CharField(max_length=1000, null=True)
    thumbnail = models.FileField(upload_to='thumbnail/', blank=True, null=True)      
    
    def delete(self, *args, **kargs):
        if self.video:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.video.path))
        if self.thumbnail:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.thumbnail.path))
        super(Video, self).delete(*args, **kargs)

    def __str__(self):
        return f'id : {self.id} / UserName : {self.uid.name} / video : {self.video}'

class Title(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20)
    eid = models.CharField(max_length=20)

    def __str__(self):
        return f'id : {self.id} / uid : {self.uid} / eid : {self.eid}'


class Daily(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.DateField()
    count = models.IntegerField()

    def __str__(self):
        return f'id : {self.id} / day : {self.day} / count : {self.count}'

class Habit(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

    def __str__(self):
        return f'id : {self.id} / title : {self.title} / content : {self.content}'

class Word(models.Model):
    id = models.AutoField(primary_key=True)
    hid = models.IntegerField()
    word = models.CharField(max_length=50)

    def __str__(self):
        return f'id : {self.id} / hid : {self.hid} / word : {self.word}'

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=50, null=True)
    content = models.TextField(null=True)
    video = models.TextField(null=True)
    time = models.TextField(null=True)
    count = models.TextField(null=True)
    list = models.TextField(null=True)
    title = models.TextField(null=True)
    contents = models.TextField(null=True)
    habitlist = models.TextField(null=True)
    wordlist = models.TextField(null=True)
    stt = models.TextField(null=True)
    emotion = models.TextField(null=True)
    emotionlist = models.TextField(null=True)
    thumbnail = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return f'id : {self.id} / uid : {self.uid}'

    
