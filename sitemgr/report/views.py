from django.shortcuts import render
from mylib.djviews import SearchView,ProcReport,Report
from django.forms import *
from report.models import YinqiQianyue,YinqiTongji
from django.views.generic import TemplateView
from django.utils import timezone

# Create your views here.
def create_list(list_type=0,count=24):
    n=timezone.now()
    y=n.year
    m=n.month-1 
    if list_type==0:
        m-=1
        return [('%s-%02d'%(x//12,x%12+1),'%s年%s月'%(x//12,x%12+1)) for x in range(y*12+m,y*12+m-count,-1)]
    else:
        m=int(n.month/3)-1
        return [('%s-%s'%(x//4,x%4+1),'%s年%s季度'%(x//4,x%4+1)) for x in range(y*4+m,y*4+m-count,-1)]

class Yinqirpt(ProcReport):
    proc_name='yinqiqushu'
    title='银企对账报送数据'
    def __init__(self,qici):
        self.params=(qici,None,None,None,None,None)
    def as_html(self):
        d=self.data
        s=['<table class="report">']
        s.append('<tr><th colspan="2">银企对账评估报告</th></tr>')
        
        s.append('<tr>')
        s.append('<th class="left">银企对账应对账户数</th>')
        s.append('<td class="number">%s</td>'%(format(self.params[1]+self.params[2],',d')))
        s.append('</tr>')

        s.append('<tr>')
        s.append('<th class="left">重点账户回收率</th>')
        s.append('<td class="number">%s</td>'%(format(self.params[3]/self.params[1],'6.2%')))
        s.append('</tr>')
        
        s.append('<tr>')
        s.append('<th class="left">一般账户回收率</th>')
        s.append('<td class="number">%s</td>'%(format(self.params[4]/self.params[2],'6.2%')))
        s.append('</tr>')
        
        s.append('<tr><th colspan="2">银行业金融机构案件防控情况统计表</th></tr>')

        s.append('<tr>')
        s.append('<th class="left">上上季应对账户数</th>')
        s.append('<td class="number">%s</td>'%(format(self.params[1]+self.params[2],',d')))
        s.append('</tr>')
        
        s.append('<tr>')
        s.append('<th class="left">超过半年未能有效对账户数</th>')
        s.append('<td class="number">%s</td>'%(format(self.params[1]+self.params[2]-self.params[3]-self.params[4],',d')))
        s.append('</tr>')
        
        s.append('<tr><th colspan="2">高管数据报送</th></tr>')

        s.append('<tr>')
        s.append('<th class="left">银企对账回收率</th>')
        s.append('<td class="number">%s</td>'%(format((self.params[3]+self.params[4])/(self.params[1]+self.params[2]),'6.2%')))
        s.append('</tr>')

        s.append('</table>')
        return '\n'.join(s)
    

class Kaohe(ProcReport):
    proc_name='kaohe'
    title='省直分行营运主管考核表'
    column_title=['分行名称','银企对账回收情况','银企对账签约率']
    column_class=[None,'number','number']
    column_format=[None,None,None]
    def __init__(self,qici):
        self.params=(qici,)
        
class LingHuo(ProcReport):
    title='灵活计息月报表'
    column_title='分行名称 本月笔数  笔数同比 笔数增幅 '\
                    ' 本月金额  金额同比  金额增幅'.split()
    column_format=[None,',.0f',',.0f','6.2%',',.2f',',.2f','6.2%']
    column_class=[None,'number','number','number','number','number','number']
    proc_name='linghuorpt'
    def __init__(self,qici):
        self.params=(qici,)

class Qianyue(Report):
    title='新开账户银企对账签约率表'
    column_title='分行号 总签约数 总账户数 本期签约  本期新开账户'.split()
    column_class=[None,'number','number','number','number']
    column_format=[None,',d',',d',',d',',d']
    def __init__(self,qici):
        self.data= YinqiQianyue.objects.values_list(
                'brno_id','qytotal','actotal','curqy','curac'
                ).filter(quater=qici)

class Yinqi(Report):
    title='银企对账回收情况统计表'
    column_title='分行号 '\
                    '重点账户 普通账户  重点发出  普通发出 '\
                    '重点收回  普通收回'.split()
    column_format=[None,',d',',d',',d',',d',',d',',d']
    column_class=[None,'number','number','number','number','number','number']
    def __init__(self,qici):
        self.data=YinqiTongji.objects.values_list(
                'brno_id','zdac','ptac','zdfc','ptfc','zdsh',
                'ptsh').filter(zhangqi=qici)
MONTH_REPORT={
    '01':LingHuo,
    }
    
QUATER_REPORT={
    '01':Kaohe,
    '02':Yinqi,
    '03':Qianyue,
    '04':Yinqirpt,
    }
        
class MonthForm(Form):
    Report_Type=[(x,MONTH_REPORT[x].title) for x in MONTH_REPORT ]
    report_type=ChoiceField(required=True,choices=Report_Type,
            label='报表种类')
    qici=ChoiceField(
        required=True,
        choices=create_list(0),
        label='报表期次')

class QuaterForm(Form):
    Report_Type=[(x,QUATER_REPORT[x].title) for x in QUATER_REPORT]
    report_type=ChoiceField(required=True,choices=Report_Type,
            label='报表种类')
    qici=ChoiceField(
        required=True,
        choices=create_list(1,8),
        label='报表期次')
    
class MonthReport(SearchView):
    paginate_by=None
    search_form_class=MonthForm
    context_object_name='report'
    template_name='report/report.html'
    keywords={'report_type':None,
        'qici':None}
    report_class=MONTH_REPORT
    def get_queryset(self):
        d=self.get_data(self.request.GET)
        self.initial=d
        t=d.get('report_type',None)
        qici=d.get('qici',None)
        if qici:
            return self.report_class[t](qici)
            
class QuaterReport(MonthReport):
    search_form_class=QuaterForm
    report_class=QUATER_REPORT
    
class HomeView(TemplateView):
    template_name='report/home.html'
    month_rpt=[(x,MONTH_REPORT[x].title) for x in MONTH_REPORT]
    quater_rpt=[(x,QUATER_REPORT[x].title) for x in QUATER_REPORT]
    month_list=create_list(0,12)
    quater_list=create_list(1,4)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['home']=self
        return self.render_to_response(context) 
    
    
    
