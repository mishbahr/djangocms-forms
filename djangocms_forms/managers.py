# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models import Count


class ActiveFormManager(models.Manager):
    def get_queryset(self):
        qs = super(ActiveFormManager, self).get_queryset()
        return qs.annotate(submission_count=Count('submissions')) \
            .filter(submission_count__gt=0)
