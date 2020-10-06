from django.shortcuts import render
from elemcore import models as emodels
from django.contrib import messages
from elemcore import forms

def show(request):
    context = {}
    form = forms.ConstructForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        if form.cleaned_data["user"] is not request.user:
            messages.add_message(request, messages.ERROR, 'Card user does not match logged in user.  Are you trying to do something sneaky?  Card not saved.')
        else:
            form.save()
            messages.add_message(request, messages.INFO, 'Card Created')


    context['form'] = form
    return render(request, 'create_card.html', context)
