# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Child(models.Model):
    indvid = models.PositiveIntegerField(unique=True, null=True)
    first_name = models.CharField(max_length=20, null=True)
    dob = models.DateField()
    email_address = models.EmailField(null=True)

    def __str__(self):
        if self.indvid:
            return str(self.indvid)
        else:
            return '{}: {}'.format(self.first_name, self.email_address)


class BirthdayMessage(models.Model):
    age = models.PositiveSmallIntegerField(primary_key=True)
    subject = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    attachment = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return "Age " + str(self.age)


class ActivityLog(models.Model):
    child = models.ForeignKey(Child)
    message = models.ForeignKey(BirthdayMessage)
    sent = models.DateTimeField(auto_now_add=True)
