from django.db import models

class HospitalInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    hname = models.CharField(max_length=50)
    hcode = models.CharField(max_length=20)
    hpost = models.CharField(max_length=50)
    haddress = models.CharField(max_length=100)
    hphone = models.CharField(max_length=20, default="")
    hurl = models.CharField(max_length=50, default="")
    hlng = models.FloatField()
    hlat = models.FloatField()

    def __str__(self):
        return f'id : {self.id} hname: {self.hname} hcode: {self.hcode} hpost: {self.hpost} haddress: {self.haddress} hphone: {self.hphone} hurl: {self.hurl} hlng: {self.hlng} hlat: {self.hlat}'

class PharmacyInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    pname = models.CharField(max_length=50)
    pcode = models.CharField(max_length=20)
    ppost = models.CharField(max_length=50)
    paddress = models.CharField(max_length=100)
    pphone = models.CharField(max_length=20, default="")
    purl = models.CharField(max_length=50, default="")
    plng = models.FloatField()
    plat = models.FloatField()

    def __str__(self):
        return f'id : {self.id} pname: {self.pname} pcode: {self.pcode} ppost: {self.ppost} paddress: {self.paddress} pphone: {self.pphone} purl: {self.purl} plng: {self.plng} plat: {self.plat}'