from django import forms

from models import Member

DOB_FORMATS = ['%m/%d/%Y', '%M/%D/%Y', '%m-%d-%Y', '%M-%D-%Y']


class SignupForm(forms.ModelForm):
    first_name = forms.CharField(error_messages={'required': 'Your first name is missing.'})
    last_name = forms.CharField(error_messages={'required': 'Your last name is missing.'})
    gender = forms.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')))
    dob = forms.DateField(error_messages={'required': 'Your birthday is missing.'}, input_formats=DOB_FORMATS)
    spouse_dob = forms.DateField(required=False, input_formats=DOB_FORMATS)
    address = forms.CharField(error_messages={'required': 'Your address is missing.'})
    city = forms.CharField(error_messages=dict(required='Your city is missing.'))
    state = forms.CharField(error_messages=dict(required='Your state is missing.'))
    postal_code = forms.CharField(error_messages=dict(required='Your zip code is missing.'))
    phone = forms.CharField(error_messages=dict(required='Your phone number is missing'))
    email = forms.CharField(error_messages=dict(required='Your email is missing.'))
    spouse_email = forms.CharField(required=False)
    spouse_phone = forms.CharField(required=False)

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'dob', 'email', 'phone', 'address', 'address2', 'city', 'state',
                  'postal_code', 'comments', 'student_class', 'dow_first_choice', 'dow_second_choice',
                  'spouse_first_name', 'spouse_last_name', 'spouse_dob', 'spouse_email', 'spouse_phone']
