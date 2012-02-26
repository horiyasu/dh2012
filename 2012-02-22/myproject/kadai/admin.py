# -*- coding: utf-8 -*-
from django.contrib import admin

from kadai.models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display =('__unicode__', 'name', 'created_at')
    list_filter = ('created_at', 'name')
    search_fields = ('name', 'content')

admin.site.register(Contact, ContactAdmin)
