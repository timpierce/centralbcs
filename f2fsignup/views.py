from copy import deepcopy
from django.shortcuts import render, get_object_or_404, get_list_or_404

from forms import SignupForm
from models import Group, Ministry


def list(request):
    ministry = request.GET.get('ministry', 'adult_education')
    kiosk = request.GET.get('kiosk', False)
    return render(request, 'f2fsignup/%s/list.html' % ministry, {'groups': get_list_or_404(Group), 'kiosk': kiosk})


def addme(request, groupid):
    ministry = request.GET.get('ministry', 'adult_education')
    kiosk = request.GET.get('kiosk', False)
    group = get_object_or_404(Group, pk=groupid)
    if not group.has_openings(ministry=ministry):
        return list(request)
    if request.method == 'POST':  # If the form has been submitted...
        form = SignupForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            member = form.save(commit=False)
            member.ministry = Ministry.objects.get(name=ministry)
            member.group = group
            member.save()
            if form.cleaned_data['spouse_first_name']:
                spouse = deepcopy(member)
                spouse.id = None
                if member.gender == 'F':
                    spouse.gender = 'M'
                elif member.gender == 'M':
                    spouse.gender = 'F'
                spouse.first_name = form.cleaned_data['spouse_first_name']
                spouse.last_name = form.cleaned_data['spouse_last_name']
                spouse.dob = form.cleaned_data['spouse_dob']
                spouse.phone = form.cleaned_data['spouse_phone']
                spouse.email = form.cleaned_data['spouse_email']
                spouse.save()
            template_parms = dict(kiosk=kiosk, group=group)
            return render(request, 'f2fsignup/%s/thanks.html' % ministry, template_parms)  # Redirect after POST
    else:
        form = SignupForm()
    return render(request, 'f2fsignup/%s/addme.html' % ministry, dict(form=form, group=group, kiosk=kiosk))
