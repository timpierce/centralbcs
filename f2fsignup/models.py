import os
from copy import deepcopy
from string import Template

from django.conf import settings
from django.core.files import File
from django.core.mail.message import EmailMessage
from django.db import models
from django.forms.models import model_to_dict
from django.utils.dateformat import DateFormat

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


# This is not the best way to do this at all
class F2FSettings(models.Model):
    start_date = models.DateField()

    def __unicode__(self):
        return 'Start Date'

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
        return self.member_set.filter(ministry=ministry).count() < settings.NUMBER_OF_MEMBERS[ministry]

    def registrant_count(self):
        return self.member_set.count()


class Member(models.Model):
    group = models.ForeignKey('Group', null=True, blank=True)  # 1
    ministry = models.CharField(default="adult_education", max_length=20)  # adult_education
    dow_first_choice = models.CharField(max_length=100, choices=dow_choices, null=True, blank=True)  # Tuesday
    dow_second_choice = models.CharField(max_length=100, choices=dow_choices, null=True, blank=True)  # Thursday
    student_class = models.CharField(max_length=100, choices=student_class_choices, null=True, blank=True)  # Senior
    first_name = models.CharField(max_length=20)  # Sally
    last_name = models.CharField(max_length=20)  # Student
    # Spouse Fields
    spouse_first_name = models.CharField(max_length=100, null=True, blank=True)
    spouse_last_name = models.CharField(max_length=100, null=True, blank=True)
    spouse_dob = models.DateField(null=True, blank=True)
    spouse_email = models.EmailField(null=True, blank=True)
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
        if self.spouse_first_name:
            spouse = deepcopy(self)
            spouse.first_name = spouse.spouse_first_name.capitalize()
            spouse.last_name = spouse.spouse_last_name.capitalize()
            spouse.dob = spouse.spouse_dob
            if self.gender == 'M':
                spouse.gender = 'F'
            else:
                spouse.gender = 'M'
            spouse.email = spouse.spouse_email
            spouse.spouse_first_name = None
            spouse.spouse_last_name = None
            spouse.spouse_dob = None
            spouse.spouse_email = None
            spouse.save()
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
            with (open(os.path.join(settings.BASE_DIR, 'templates/signup/email/member.eml'), 'rb')) as f:
                email_text = File(f).read()
            start_date_text = DateFormat(F2FSettings.objects.all()[0].start_date).format('F jS')
            email_parms = model_to_dict(self.group)
            email_parms['first_name'] = self.first_name
            email_parms['start_date'] = start_date_text
            message = EmailMessage()
            message.to = [self.email]
            message.from_email = settings.STAFF_NOTIFICATION_EMAIL
            message.content = Template(email_text).substitute(email_parms)
            message.subject = 'Face to Face Group Information'
            message.send(fail_silently=True)
