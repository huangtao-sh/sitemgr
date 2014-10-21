#!/usr/bin/python3
import os
import sys
import re
from mylib.pdf import read_pdf
from datetime import date
if sys.platform.startswith('linux'):
    DOC_ROOT='~/文档/工作平台/办公室文件'
else:
    DOC_ROOT='~/documents/工作平台/办公室文件'
DOC_PATH=''
URL_ROOT='/officedoc'
BASE_DIR='~/mysite/workmgr'
sys.path.append(os.path.expanduser(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "workmgr.settings")
from documents.models import Office,Tag,Document

def join(*args):
    return os.path.join(*args).replace('\\','/')

pattern=re.compile('\s*?(?P<office>\w*?)'\
        r'[〔|\[](?P<year>\d{4})[〕|\]]'\
        r'(?P<no>\d+)号'\
        r'\s*?(?P<name>.*)'
        )
        
qianfa=re.compile(r'(?P<office>\w*?)'\
            r'(?P<year>\d{4})年'\
            r'(?P<month>\d{1,2})月'\
            r'(?P<date>\d{1,2})日印发')

doc_root=join(os.path.expanduser(DOC_ROOT),DOC_PATH)
url_root=join(URL_ROOT,DOC_PATH)
create_list=[]
doc=Document.objects
for root,dirs,files in os.walk(doc_root):
    for f in files:
        file_path=join(root,f)
        rela_path=root.replace(doc_root,'')
        url_path=join(url_root,rela_path,f)
        base_name,ext=os.path.splitext(f)
        if not((base_name.find('附件')>-1)or
                (base_name.find('附表')>-1)):
            try:
                d=Document.objects.get(file_name=url_path)
            except:
                k=pattern.match(base_name)
                if k:
                    office=k.group('office')
                    year=k.group('year')
                    no=k.group('no')
                    name=k.group('name')
                    efficetive_date=None
                    jigou=None
                    if ext.upper()=='.PDF':
                        for l in read_pdf(file_path):
                            l=l.strip().replace(' ','')
                            p=qianfa.match(l)
                            if p:
                                efficetive_date=date(int(p.group('year')),
                                    int(p.group('month')),int(p.group('date')))
                                jigou=p.group('office')
                               
                    off,created=Office.objects.get_or_create(code=office)
                    if created:
                        off.name=jigou if jigou else '交通银行'
                        off.save()
                    d=Document(code=off,year=year,number=no,\
                        name=name,file_name=url_path,
                        efficetive_date=efficetive_date)
                    create_list.append(d)
Document.objects.bulk_create(create_list)



                
                

