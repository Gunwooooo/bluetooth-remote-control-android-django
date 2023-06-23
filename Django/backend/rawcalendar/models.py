from django.db import models
class RawCalendar(models.Model):
    cid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=20)
    rawStringList = models.TextField(null=True)

    # def __str__(self):
    #     return f'uid : {self.uid} password: {self.password} name: {self.name} check_protector: {self.protector_check} protector: {self.protector_id}'



