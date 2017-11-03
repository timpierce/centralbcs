from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput

from models import Child

DOB_FORMATS = ['%m/%d/%Y', '%M/%D/%Y', '%m-%d-%Y', '%M-%D-%Y', '%m/%d/%y']


#  Todo: Throw validation error if age is less than 18
class AddChildForm(forms.ModelForm):
    first_name = forms.CharField(
        error_messages={'required': "The child's first name is required."},
    )
    dob = forms.DateField(
        error_messages=dict(required="The child's birthday is required."),
        input_formats=DOB_FORMATS,
    )
    email_address = forms.CharField(
        error_messages=dict(required="Parent's email address is required."),
    )

    class Meta:
        model = Child
        fields = ['first_name', 'dob', 'email_address',]
