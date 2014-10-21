from django.db.models import *

# Create your models here.
class SigCard(Model):
    cardno=CharField(
        max_length=8,
        primary_key=True)
    pwd=CharField(
        max_length=8
        )
    No=IntegerField()
    def __str__(self):
        return self.cardno
        
class Branch(Model):
    branchno=CharField(
        max_length=6,
        primary_key=True
        )
    bdt=DateField()
    edt=DateField()
    branchname=CharField(
        max_length=20)
    level=CharField(
        max_length=1)
    superior=CharField(
        max_length=6)
    order=IntegerField(
        null=True)
    def __str__(self):
        return self.branchno
    def prov_name(self):
        if self.branchno==self.superior:
            return self.branchname
        else:
            b=Branch.objects.values('branchname').get(branchno=self.superior)
            return b['branchname']
    @classmethod
    def prov_list(cls):
        return cls.objects.values_list('branchno','branchname','order').filter(
            level__range=[1,2],
            branchno__lt='800999').exclude(branchno='312999')

class JiGou(Model):
    branchno=CharField(
        max_length=6,
        primary_key=True)
    dbt=DateField()
    edt=DateField()
    branchname=CharField(
            max_length=30)
    address=CharField(
            max_length=50,
            null=True)
    level=CharField(
            max_length=1)
    brtype=CharField(
            max_length=1)
    brclass=CharField(max_length=1)
    branch=ForeignKey(Branch)
    zhongxin=CharField(
            max_length=6,
            null=True)
    mode=CharField(
            max_length=1,
            null=True)
    superior=CharField(
            max_length=6,
            null=True)
    yidi=CharField(
            max_length=1,
            null=True)
    tellerlevel=CharField(
            max_length=1,
            null=True)
    kaihu=CharField(
            max_length=6,
            null=True)
    guoji=CharField(
            max_length=12,
            null=True)
    lixishui=CharField(
        max_length=6,
        null=True)
    sunyi=CharField(
            max_length=6,
            null=True)
    tel=CharField(
            max_length=20,
            null=True)
    def __str__(self):
        return self.branchno
    def prov_no(self):
        return self.branch.superior
    def prov_name(self):
        return self.branch.prov_name()

class YinqiTongji(Model):
    zhangqi=CharField(
        max_length=6
        )
    brno=ForeignKey(Branch)
    zdac=BigIntegerField()
    ptac=BigIntegerField()
    zdfc=BigIntegerField()
    ptfc=BigIntegerField()
    zdsh=BigIntegerField()
    ptsh=BigIntegerField()
    zdwd=BigIntegerField(null=True)
    ptwd=BigIntegerField(null=True)
    zdwdwt=BigIntegerField(null=True)
    ptwdwt=BigIntegerField(null=True)
    zdtxwt=BigIntegerField(null=True)
    pttxwt=BigIntegerField(null=True)
    zdtxhs=BigIntegerField(null=True)
    pttxhs=BigIntegerField(null=True)
    drtime=DateTimeField()
    memo=CharField(max_length=100,null=True)
    def __str__(self):
        return self.brno

class YinqiQianyue(Model):
    quater=CharField(max_length=6)
    brno=ForeignKey(Branch)
    qytotal=BigIntegerField(null=True)
    actotal=BigIntegerField(null=True)
    curqy=BigIntegerField(null=True)
    curac=BigIntegerField(null=True)
    def __str__(self):
        return self.brno
            
class Linghuo(Model):
    month=CharField(
        max_length=7
        )
    brno=ForeignKey(Branch)
    ccy=CharField(max_length=3)
    account=BigIntegerField()
    cardcount=BigIntegerField()
    amount=DecimalField(
        max_digits=13, decimal_places=2)
    def __str__(self):
        return self.brno
        
        
    
        
        

