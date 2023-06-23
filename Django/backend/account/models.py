from django.db import models

class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    protector_check = models.BooleanField(default=False)
    protector_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'uid : {self.uid} password: {self.password} name: {self.name} check_protector: {self.protector_check} protector: {self.protector_id}'




