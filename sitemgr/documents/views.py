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

from documents.models import Document,Office,Tag
from django.forms import *
from mylib.djviews import SearchView
# Create your views here.
class SearchForm(ModelForm):
    class Meta:
        model=Document
        fields=['code','year','number','name','tags']

class HomeView(SearchView):
    model=Document
    context_object_name='object_list'
    template_name='documents/document_search.html'
    keywords={'code':None,
            'year':None,
            'number':None,
            'name':'contains',
            'tags':None,
            } 
    search_form_class=SearchForm
    ordering=['-year','-efficetive_date','code','-number']
    



