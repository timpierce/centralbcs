# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import BirthdayMessage

admin.site.register(BirthdayMessage)
admin.site.site_header = 'Central Baptist Church'
admin.site.site_title = 'Central Baptist Church'
