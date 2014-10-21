from django.forms import *
from django.views.generic import FormView
try:
    from xlrd3 import *
except:
    pass
import os
from django.http import HttpResponseRedirect,HttpResponse
from django.db import connection
from txl.models import Address
from django.db.models import Q

def float2str(data,keys):
    for key in keys:
        if(key in data)and isinstance(data[key],float):
            data[key]=str(int(data[key]))

def split_data(data,step=10000):
    b,e=0,0
    count=len(data)
    for e in range(step,count,step):
        yield data[b:e]
        b=e
    if e<count:
        yield data[e:count]

class ImportBase:
    title=None
    def clear(self):
        return (None,None)
        
    def process(self,filename):
        self.rows=0
        try:
            self.openfile(filename)
            d=[]
            for self.curline in range(self.rows):
                a=self.getline()
                if a:
                    d.append(a)
        finally:
            self.closefile()
        return d
    
    def openfile(self,filename):
        pass
    
    def getline(self):
        return False
    
    def closefile(self):
        pass

class ImportExcel(ImportBase):
    def value(self,i):
        cell=self.ws.cell(self.curline,i)
        if cell.ctype in(1,2):
            v=cell.value
        elif cell.ctype==3:
            if cell.has_date:
                v=cell.date()
            else:
                v=cell.time()
        else:
            v=None
        if v:
            return v
    
    def openfile(self,filename):
        self.onopen()
        self.wb=open_workbook(file_contents=filename.read())
        self.ws=self.wb.sheet_by_name(self.sheetname)
        self.rows=self.ws.nrows
    
    def onopen(self):
        pass

class yjkmm(ImportBase):
    title='印鉴卡密码'
    sql='replace into report_sigcard(no,cardno,pwd) values(%s,%s,%s)'
    def process(self,filename):
        from mylib.stdlib import decode_file
        d=[]
        
        for r in decode_file(filename.read()):
            k=r.split()
            if(len(k)==3)and(k[1].isdigit()):
                d.append(k)
        return d

class yqdz(ImportExcel):
    title='银企对账统计表'

    BRANCH={
    "交通银行安徽省分行":"341999",
    "交通银行北京市分行":"110999",
    "交通银行大连分行":"212999",
    "交通银行福建省分行":"351999",
    "交通银行甘肃省分行":"621999",
    "交通银行广东省分行":"441999",
    "交通银行广西区分行":"451999",
    "交通银行贵州省分行":"521999",
    "交通银行海南省分行":"461999",
    "交通银行河北省分行":"131999",
    "交通银行河南省分行":"411999",
    "交通银行黑龙江省分行":"231999",
    "交通银行湖北省分行":"421999",
    "交通银行湖南省分行":"431999",
    "交通银行吉林省分行":"221999",
    "交通银行江苏省分行":"320999",
    "交通银行江西省分行":"361999",
    "交通银行辽宁省分行":"211999",
    "交通银行内蒙古区分行":"151999",
    "交通银行宁波分行":"332999",
    "交通银行宁夏区分行":"641999",
    "交通银行青岛分行":"372999",
    "交通银行青海省分行":"631999",
    "交通银行厦门分行":"352999",
    "交通银行山东省分行":"371999",
    "交通银行山西省分行":"141999",
    "交通银行陕西省分行":"611999",
    "交通银行上海市分行":"310999",
    "交通银行深圳分行":"443999",
    "交通银行四川省分行":"511999",
    "交通银行苏州分行":"325999",
    "交通银行天津市分行":"120999",
    "交通银行无锡分行":"322999",
    "交通银行云南省分行":"531999",
    "交通银行浙江省分行":"331999",
    "交通银行新疆维吾尔自治区分行":"651999",
    "交通银行重庆市分行":"500999"}
    
    def onopen(self):
        self.sheetname='企银对账统计表'
        self.sql='insert into report_yinqitongji '\
        '(zhangqi,brno_id,zdac,ptac,zdfc,ptfc,zdsh,ptsh,zdwd,ptwd,zdwdwt,ptwdwt,zdtxwt,pttxwt,zdtxhs,pttxhs,drtime,memo)'\
        'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        
    def clear(self):
        return ('delete from report_yinqitongji where zhangqi=%s',(self.zq,))
        
    def openfile(self,filename):
        super().openfile(filename)
        n,e=os.path.splitext(filename.name)
        self.zq=n[-6:]
    
    def getline(self):
        s=[self.zq]
        brname=self.value(0)
        if brname in self.BRANCH:
            s.append(self.BRANCH[brname])
            for i in (1,2,3,4,7,8,11,12,13,14,15,16,17,18,21,0):
                s.append(self.value(i))
            return s

class Yinqi(ImportExcel):
    title='电子对账签约情况统计表'
    sql='insert into report_yinqiqianyue(quater,brno_id,qytotal,actotal,curqy,curac) '\
                'values(%s,%s,%s,%s,%s,%s)'
    def clear(self):
        return ('delete from report_yinqiqianyue where quater=%s',(self.date,))
        
    def onopen(self):
        self.sheetname='电子对账签约情况表'
        
    def openfile(self,filename):
        super().openfile(filename)
        n,e=os.path.splitext(filename.name)
        self.date=n[-6:]
        
    def getline(self):
         brno=self.value(1)
         if brno and(len(brno)==11):
             brno=brno[2:8]
             s=[self.date,brno,self.value(3),self.value(4),\
                     self.value(6),self.value(7)]
             return s

class Txl(ImportExcel):
    title='通讯录'
    field_list=('name','department','mobile','company','tel','memo',\
        'email')
    
    def process(self,filename):
        book=open_workbook(file_contents=filename.read())
        for sheet in book.sheets():
            self.proc_sheet(sheet)
            
    def proc_sheet(self,sheet):
        fields={}
        for r in range(sheet.nrows):
            l=sheet.row_values(r)
            if 'title' in l:
                for i in range(sheet.ncols):
                    if l[i] in self.field_list:
                        fields[l[i]]=i
            elif fields:
                p={}
                for k in fields:
                    if l[fields[k]]:
                        p[k]=l[fields[k]]
                if 'name' in p:
                    float2str(p,['mobile','tel','memo'])
                    try:
                        if 'mobile' in p:
                            q=Q(mobile=p['mobile'])
                        elif 'email' in p:
                            q=Q(email=p['email'])
                        a=Address.objects.get(q)
                        for k in p:
                            if hasattr(a,k):
                                setattr(a,k,p[k])
                        a.save()
                    except:
                        Address.objects.create(**p)        
    
    
class linghuo(ImportExcel):
    title='灵活计息月报表'
    CCY={
            '人民币':'CNY',
            '美元':'USD',
            '港币':'HKD',
            '欧元':'EUR',
        }
        
    sql='insert into report_linghuo '\
            '(month,brno_id,ccy,account,cardcount,amount)'\
                'values(%s,%s,%s,%s,%s,%s)'
    def clear(self):
        return ('delete from report_linghuo where month=%s',(self.date,))
        
    def onopen(self):
        self.sheetname='灵活计息业务量统计表'
        
    def openfile(self,filename):
        super().openfile(filename)
        n,e=os.path.splitext(filename.name)
        self.date=n[-7:]
        
    def getline(self):
        brno=self.value(0)
        if brno:
            if len(brno)==11:
                brno=brno[2:8]
            elif len(brno)==6:
                pass
            else:
                return
            s=[self.date,brno,self.CCY[self.value(2)],
                    self.value(3),self.value(4),self.value(5)]
            return s

IMPORTTYPE={
            '01':yjkmm,
            '02':yqdz,
            '03':Yinqi,
            '04':linghuo,
            '05':Txl,
            }

class ImportForm(Form):
    Import_Type=[(x,IMPORTTYPE[x].title) for x in sorted(IMPORTTYPE)]
    import_type=ChoiceField(required=True,choices=Import_Type,
            label='上传文件类型')
    file=FileField(required=True,
            label='请选择文件')    
            
class UploadView(FormView):
    form_class=ImportForm
    template_name='upload.html'
    cursor=connection.cursor()
    def form_valid(self,form):
        tp=form.cleaned_data['import_type']
        imp=IMPORTTYPE[tp]()
        for key in form.files:
            d=imp.process(form.files[key])
            if d:
                sql,params=imp.clear()
                if sql:
                    self.cursor.execute(sql,params)
                for params in d:
                    try:
                        self.cursor.execute(imp.sql,params)
                    except:
                        continue
        self.log=['类型：%s'%(tp)]
        return HttpResponse('\n'.join(self.log))
