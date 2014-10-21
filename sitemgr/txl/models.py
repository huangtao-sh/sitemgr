from django.db import models

# Create your models here.
class Address(models.Model):
    name = models.CharField(max_length=40,verbose_name='姓名')
    spell = models.CharField(max_length=40,
            verbose_name='拼写',
            null=True,
            blank=True)
    company = models.CharField(max_length = 50,
            verbose_name='单位',
            null=True,
            blank=True)
    department = models.CharField(max_length=50,
            verbose_name='部门',
            null=True,
            blank=True)
    mobile = models.CharField(max_length=11,
            verbose_name='手机',
            null=True,blank=True)
    tel = models.CharField(max_length=30,
            verbose_name='电话',null=True,blank=True)
    email = models.EmailField(verbose_name='电子邮件',null=True,blank=True)
    memo = models.CharField(max_length=100,
            verbose_name='备注',
            null=True,blank=True)
    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        self.spell='abc'
        super().save(*args,**kwargs)
