from django.shortcuts import render

from forms import AddChildForm


def addchild(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = AddChildForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            form.save()
            return render(request, 'faithpath/thanks.html')  # Redirect after POST
    else:
        form = AddChildForm()
    return render(request, 'faithpath/addchild.html', dict(form=form))
