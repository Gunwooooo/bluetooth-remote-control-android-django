from rest_framework import serializers

from .models import User, IntroList, Question, MyChatting, Video, Title, Card, Result

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class IntroListSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroList
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class MyChattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyChatting
        fields = '__all__'
        
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

