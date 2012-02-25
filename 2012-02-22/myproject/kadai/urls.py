# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'kadai.views.index', name='kadai_index'),
    url(r'kadai1/$', 'kadai.views.kadai1', name='kadai_kadai1'),
    url(r'kadai2/$', 'kadai.views.kadai2', name='kadai_kadai2'),
    url(r'kadai3/$', 'kadai.views.kadai3', name='kadai_kadai3'),
    url(r'kadai3_thanks/$', 'kadai.views.kadai3_thanks', name='kadai_kadai3_thanks'),
    )
