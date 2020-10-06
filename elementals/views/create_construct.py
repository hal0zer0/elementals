from django.shortcuts import render
from elemcore import models as emodels
from django.contrib import messages
from elemcore import forms, validators, exceptions


def show(request):
    context = {}
    errored = False
    form = forms.ConstructForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        print("form valid")
        try:
            v = validators.ConstructValidator()
            v.validate(form.cleaned_data)
        except exceptions.ConstructValidationError as err:
            messages.add_message(request, messages.INFO, err)
            errored = True

        if not errored:
            form.save()
            print('form saved')
            messages.add_message(request, messages.INFO, 'Card Created')
    else:
        print("ok what the form's invalid")

    context['form'] = form
    return render(request, 'create_card.html', context)
