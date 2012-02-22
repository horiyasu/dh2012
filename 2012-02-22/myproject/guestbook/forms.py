# -*- coding: utf-8 -*-
from django import forms

from guestbook.models import Greeting

class GreetingForm(forms.ModelForm):
    """
    ゲストブックの書き込みフォーム
    モデルを元に生成する
    """
    class Meta:
        model = Greeting

        # 書き込み日時は除く
        exclude = ('created_at')

