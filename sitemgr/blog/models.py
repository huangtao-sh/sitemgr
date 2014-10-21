#  models.py
#  
#  Copyright 2014 huangtao <huangtao.jh@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from django.db.models import *
from django.contrib.auth.models import User
from django.utils.encoding import force_text
# Create your models here.

class Tag(Model):
    name=CharField(
        max_length=10,
        verbose_name='标签')


class Entry(Model):
    title=CharField(
        max_length=100,
        verbose_name='标题'
        )
    author=ForeignKey(User,
        verbose_name='作者'
        )
    create_date=DateTimeField(
        verbose_name='创建时间',
        null=True,
        blank=True)
        
    update_date=DateTimeField(
        verbose_name='修改时间',
        null=True,
        blank=True)
    content=TextField(
        verbose_name='内容')
    tags=ManyToManyField(Tag,
        verbose_name='标签',
        null=True,
        blank=True)
    
    def __str__(self):
        return self.title
    
    def as_html(self):
        import markdown
        return markdown.markdown(self.content).join([
            "<div class='blog'>","</div>"]) 
    
        
    
        
        
