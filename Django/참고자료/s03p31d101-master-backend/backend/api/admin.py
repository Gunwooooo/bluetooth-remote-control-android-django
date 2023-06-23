from django.contrib import admin

from .models import User
from .models import IntroList
from .models import Introduction
from .models import Question
from .models import Interview
from .models import Board
from .models import List
from .models import Card
from .models import Chatting
from .models import MyChatting
from .models import Video
from .models import Title
from .models import Daily
from .models import Word
from .models import Habit
from .models import Result

admin.site.register(Word)
admin.site.register(Habit)
admin.site.register(User)
admin.site.register(IntroList)
admin.site.register(Introduction)
admin.site.register(Question)
admin.site.register(Interview)
admin.site.register(Board)
admin.site.register(List)
admin.site.register(Card)
admin.site.register(Chatting)
admin.site.register(MyChatting)
admin.site.register(Video)
admin.site.register(Title)
admin.site.register(Daily)
admin.site.register(Result)


# Register your models here.
