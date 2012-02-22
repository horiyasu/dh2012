# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from datetime import date

from kadai.models import Contact
from kadai.forms import ContactForm

def index(request):
    ctxt = RequestContext(request,{
    })
    return render_to_response('kadai/index.html', ctxt)

def kadai1(request):
    ctxt = RequestContext(request,{
        "today" : date.today(),
        "number" : 2**10
    })
    return render_to_response('kadai/kadai1.html', ctxt)

def kadai2(request):
    dim1 = int(request.GET.get('dim1',0))
    dim2 = int(request.GET.get('dim2',0))
    sum = dim1 + dim2
    ctxt = RequestContext(request,{
        "dim1" : dim1,
        "dim2" : dim2,
        "sum" : sum,
    })
    return render_to_response('kadai/kadai2.html', ctxt)

def kadai3(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = ContactForm()
        ctxt = RequestContext(request,{"form":form})
        return render_to_response('kadai/kadai3.html', ctxt)




