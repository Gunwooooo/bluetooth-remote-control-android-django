from django.db import models

class Alarm(models.Model):
    aid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20)
    morning = models.CharField(max_length=50,default="00 : 00")
    afternoon = models.CharField(max_length=50, default="00 : 00")
    evening = models.CharField(max_length=50, default="00 : 00")
    morning_switch = models.BooleanField(default=False)
    afternoon_switch = models.BooleanField(default=False)
    evening_switch = models.BooleanField(default=False)

    # def __str__(self):
    #     return f'uid : {self.uid} password: {self.password} name: {self.name} check_protector: {self.protector_check} protector: {self.protector_id}'



