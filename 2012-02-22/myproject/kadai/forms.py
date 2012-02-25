# -*- coding: utf-8 -*-

from django.forms import ModelForm
from kadai.models import Contact

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('created_at',)
