# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.views.generic.create_update import create_object

from guestbook.models import Greeting
from guestbook.forms import GreetingForm

def index(request):
    # 汎用ビューを利用
    return create_object(request,
                        form_class=GreetingForm,
                        post_save_redirect=reverse('guestbook_index')
                        ,extra_context={'greeting_list':Greeting.objects.all()})
