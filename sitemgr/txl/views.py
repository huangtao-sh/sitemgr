from django.shortcuts import render
from django.forms import *
from txl.models import Address
from mylib.djviews import SearchView
from django.views.generic import FormView
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q

# Create your views here.
class SearchForm(ModelForm):
    class Meta:
        model=Address
        fields=('spell','name','mobile','tel')

class Search(SearchView):
    model=Address
    context_object_name='object_list'
    template_name='txl/address_search.html'
    keywords={
            'spell':'icontains',
            'mobile':'contains',
            'name':'contains',
            'tel':'contains',
            } 
    search_form_class=SearchForm
    ordering=['name']
    
class HomeView(Search):
    paginate_by=None
    template_name='txl/address_home.html'
