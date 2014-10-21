#  views.py
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

from django.shortcuts import render
from blog.models import *
from django.views.generic.edit import ModelFormMixin
from django.views.generic import ListView,DetailView,CreateView,\
        UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.forms import *
from mylib.djviews import SearchView
from django.utils import timezone
# Create your views here.

FIELDS=['title','author','content','tags']
HOME_URL=reverse_lazy('blog:home')
class BlogCreate(CreateView):
    model=Entry
    fields=FIELDS
    success_url=HOME_URL
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.create_date=timezone.now()
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)
   
class BlogDetail(DetailView):
    model=Entry

class BlogUpdate(UpdateView):
    model=Entry
    fields=FIELDS
    success_url=HOME_URL
    def form_valid(self,form):
         self.object=form.save(commit=False)
         self.object.update_date=timezone.now()
         self.object.save()
         return super(ModelFormMixin, self).form_valid(form)

class BlogDelete(DeleteView):
    model=Entry
    success_url=HOME_URL
    template_name='base_confirm_delete.html'

class HomeView(SearchView):
    model=Entry
    context_object_name='object_list'
    template_name='blog/entry_home.html'
    ordering=['-create_date']
    search_form_class=None
    
    
    
