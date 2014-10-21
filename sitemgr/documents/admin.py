from django.contrib import admin

# Register your models here.
from documents.models import *
# Register your models here.
admin.site.register(Document)
admin.site.register(Office)
admin.site.register(Tag)
