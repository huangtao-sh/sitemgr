from django.db import models

# Create your models here.
class Office(models.Model):
    code = models.CharField(max_length=10,verbose_name='发文字')
    name = models.CharField(max_length=50,verbose_name='发文机关')
    def __str__(self):
        return self.code

class Tag(models.Model):
    name = models.CharField(max_length=10,verbose_name='标签')
    def __str__(self):
        return self.name

class Document(models.Model):
    code = models.ForeignKey(Office,verbose_name='发文机关')
    year = models.CharField(max_length=4,verbose_name='发文年份')
    number = models.IntegerField(verbose_name='序号')
    name = models.CharField(max_length=100,verbose_name='文件名称')
    file_name=models.CharField(max_length=255,verbose_name='文件路径')
    tags=models.ManyToManyField(Tag,verbose_name='标签')
    efficetive_date=models.DateField(null=True,
        verbose_name='生效日期',blank=True)
    expire_date=models.DateField(null=True,verbose_name='失效日期',
        blank=True)
    def office_no(self):
        return '%s〔%s〕%s号'%(self.code.code,self.year,self.number)
    def is_efficetive(self):
        return not self.expire_date
    def __str__(self):
        return ' '.join([self.office_no(),self.name])


    
