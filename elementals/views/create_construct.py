from django.shortcuts import render, redirect
from django.contrib import messages
from elemcore import forms, validators, exceptions


def show(request):
    context = {}
    errored = False
    form = forms.ConstructForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        try:
            v = validators.ConstructValidator()
            v.validate(form.cleaned_data)
        except exceptions.ConstructValidationError as err:
            messages.add_message(request, messages.INFO, err)
            errored = True
        if not errored:
            construct = form.save()
            return redirect("abilities", construct_id=construct.id)
            messages.add_message(request, messages.INFO, 'Card Created')


    context['form'] = form
    return render(request, 'create_construct.html', context)
