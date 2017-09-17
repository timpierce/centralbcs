import os
from string import Template

from django.conf import settings
from django.core.files import File
from django.core.mail.message import EmailMessage
from django.db import models
from django.forms.models import model_to_dict
from django.utils.dateformat import format
from datetime import datetime

dow_choices = (('Sunday', 'Sunday'),
               ('Monday', 'Monday'),
               ('Tuesday', 'Tuesday'),
               ('Thursday', 'Thursday'))

student_class_choices = (('Freshman', 'Freshman'),
                         ('Sophomore', 'Sophomore'),
                         ('Junior', 'Junior'),
                         ('Senior', 'Senior'),
                         ('Grad Student', 'Grad Student'))


class ImportFile(models.Model):
    data_file = models.FileField()

    def __unicode__(self):
        return self.data_file.name


class Ministry(models.Model):
    name = models.CharField(max_length=255)
    limit = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'ministries'


class F2FSettings(models.Model):
    attribute = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.attribute

    class Meta:
        verbose_name = "F2F Setting"


class Group(models.Model):
    name = models.CharField(max_length=100)  # Benson/Pierce
    hosts = models.CharField(max_length=100)  # Tim and Jessica Pierce
    leaders = models.CharField(max_length=100, null=True, blank=True)  # Guy Benson
    leader_email = models.EmailField()  # guy.benson@email.com
    leader_phone = models.CharField(max_length=15)  # (979) 555-5555
    day_of_week = models.CharField(max_length=100, choices=dow_choices)  # Thursday
    location = models.CharField(max_length=100)  # Cole Creek Estates (HWY 30)
    address = models.CharField(max_length=500)  # 11525 Deer Creek Dr., College Station, TX
    order_field = models.IntegerField()

    class Meta:
        ordering = ["order_field"]

    def __unicode__(self):
        return self.name

    def has_openings(self, ministry):
        ministry = Ministry.objects.get(name=ministry)
        return self.member_set.filter(ministry=ministry).count() < ministry.limit

    def registrant_count(self):
        return self.member_set.count()


class Member(models.Model):
    group = models.ForeignKey('Group', null=True, blank=True)  # 1
    ministry = models.ForeignKey('Ministry')  # adult_education
    student_class = models.CharField(max_length=100, choices=student_class_choices, null=True, blank=True)  # Senior
    first_name = models.CharField(max_length=20)  # Sally
    last_name = models.CharField(max_length=20)  # Student
    gender = models.CharField(max_length=1)  # M or F
    dob = models.DateField()  # 1/1/80
    email = models.EmailField()  # student@tamu.edu
    phone = models.CharField(max_length=20)  # (555) 555-5555
    address = models.CharField(max_length=100)  # 123 Main Street
    address2 = models.CharField(max_length=100, blank=True, null=True)  # Apt. 1
    city = models.CharField(max_length=30)  # College Station
    state = models.CharField(max_length=20, default='TX')  # TX
    postal_code = models.CharField(max_length=20)  # 77840
    comments = models.CharField(max_length=400, null=True, blank=True)  # Can't wait to attend!!!
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    send_member_email = models.BooleanField(default=True)

    def name(self):
        return "%s %s" % (self.first_name, self.last_name)  # Sally Student

    name.admin_order_field = 'last_name'

    def __unicode__(self):
        return self.name()

    def save(self, send_email=True, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        new_group_member = False
        if self.group:  # a group is assigned
            if self.pk:  # on update
                old_obj = Member.objects.get(pk=self.pk)
                if old_obj.group != self.group:  # if group has changed
                    new_group_member = True
            else:  # on insert
                new_group_member = True
        super(Member, self).save(args, kwargs)

        """ Send email notification to member if they have been assigned to a new group """
        if new_group_member and send_email and self.send_member_email:
            with (open(os.path.join(settings.BASE_DIR, 'templates/f2fsignup/email/member.eml'), 'rb')) as f:
                email_text = File(f).read()
            start_date = F2FSettings.objects.get(attribute='start_date').value
            start_date_text = format(datetime.strptime(start_date, '%m/%d/%Y'), 'F jS')
            email_parms = model_to_dict(self.group)
            email_parms['first_name'] = self.first_name
            email_parms['start_date'] = start_date_text
            message = EmailMessage()
            message.to = [self.email]
            message.from_email = settings.STAFF_NOTIFICATION_EMAIL
            message.body = Template(email_text).substitute(email_parms)
            message.subject = 'Face to Face Group Information'
            message.send(fail_silently=True)
