# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.dispatch import Signal

to_create_verify = Signal(providing_args=["target", "category", "name", "content", "user"])
on_notify_verify_owner = Signal(providing_args=["instance"])
