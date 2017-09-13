from datetime import datetime
from string import Template

from django.conf import settings
from django.core.files import File
from django.core.mail import send_mail
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.dateformat import DateFormat

from forms import SignupForm
from models import Group, F2FSettings


def list(request):
    ministry = request.GET.get('ministry', 'adult_education')
    kiosk = request.GET.get('kiosk', False)
    if settings.GROUP_SIGNUP_ACTIVE:
        return render(request, 'signup/%s/list.html' % ministry, {'groups': get_list_or_404(Group), 'kiosk': kiosk})
    else:
        return addme(request, -1)


def addme(request, groupid):
    ministry = request.GET.get('ministry', 'adult_education')
    kiosk = request.GET.get('kiosk', False)
    if settings.GROUP_SIGNUP_ACTIVE:
        group = get_object_or_404(Group, pk=groupid)
        if (not group.has_openings(ministry=ministry)):
            return list(request)
    if request.method == 'POST':  # If the form has been submitted...
        form = SignupForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            member = form.save(commit=False)
            member.ministry = ministry
            if settings.GROUP_SIGNUP_ACTIVE:
                member.group = group
            member.save()
            if settings.GROUP_SIGNUP_ACTIVE is False:
                # with (open('templates/signup/email/member.eml', 'rb')) as f:
                #    email_text = File(f).read()
                #    email_parms = model_to_dict(group)
                #    email_parms['first_name'] = member.first_name
                #    email_parms['start_date'] = settings.GROUP_START_DATE_TEXT
                #    send_mail('Face 2 Face Group Information', Template(email_text).substitute(email_parms), settings.STAFF_NOTIFICATION_EMAIL, [member.email], fail_silently=False)
                # else:
                with (open('/home/piercegs/webapps/f2f/f2f/templates/signup/email/staff.eml', 'rb')) as f:
                    email_text = File(f).read()
                    email_parms = model_to_dict(member)
                    email_parms['dob'] = datetime.strftime(member.dob, '%m/%d/%Y')
                    send_mail('New Face 2 Face registration', Template(email_text).substitute(email_parms),
                              settings.STAFF_NOTIFICATION_EMAIL, [settings.STAFF_NOTIFICATION_EMAIL],
                              fail_silently=True)
            start_date_text = DateFormat(F2FSettings.objects.all()[0].start_date).format('F jS')
            template_parms = dict(kiosk=kiosk, start_date=start_date_text)
            if settings.GROUP_SIGNUP_ACTIVE:
                template_parms['group'] = group
                template_parms['start_date'] = start_date_text
            return render(request, 'signup/%s/thanks.html' % ministry, template_parms)  # Redirect after POST
    else:
        form = SignupForm()
    if settings.GROUP_SIGNUP_ACTIVE:
        return render(request, 'signup/%s/addme.html' % ministry, dict(form=form, group=group, kiosk=kiosk))
    else:
        return render(request, 'signup/%s/addme.html' % ministry, dict(form=form, kiosk=kiosk))
