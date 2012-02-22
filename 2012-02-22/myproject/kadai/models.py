# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

class Contact(models.Model):
    name = models.CharField(u'名前',max_length=50)
    content = models.TextField(u'内容', max_length=1000)
    created_at = models.DateTimeField(u'問い合わせ日時', default=datetime.now)

    def __unicode__(self):
        """
        モデルの文字列表現
        内容の改行を削除して先頭から２０文字を返す
        """
        return self.name + ":"+''.join(unicode(self.content).splitlines())[:20]

    class Meta:
        # ソート順
        ordering = ('-created_at',)
        # 単数形
        verbose_name = u'問い合わせ'
        # 複数形
        verbose_name_plural=u'問い合わせ'