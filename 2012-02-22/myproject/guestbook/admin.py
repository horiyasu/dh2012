# -*- coding: utf-8 -*-
from django.contrib import admin

from guestbook.models import Greeting

class GreetingAdmin(admin.ModelAdmin):
    list_display =('__unicode__', 'username', 'created_at')
    list_filter = ('created_at', 'username')
    search_fields = ('username', 'content')

admin.site.register(Greeting, GreetingAdmin)
