# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from six import text_type

from . import models

def target_records(target, **kwargs):
    qset = models.Verify.objects.filter(**kwargs)
    if isinstance(target, text_type):
        ct = ContentType.objects.get_by_natural_key(*target.split('.'))
        return qset.filter(target_type=ct)
    ct = ContentType.objects.get_for_model(target)
    return qset.filter(target_id=target.id, target_type=ct)
