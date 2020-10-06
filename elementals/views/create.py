from django.shortcuts import render
from elemcore import models as emodels
from django.contrib import messages
from elemcore import forms

def show(request):
    context = {}
    form = forms.ConstructForm(request.POST or None, initial={'user': request.user})
    if form.is_valid():
        #form.cleaned_data["user_id"] = request.user.id
        form.save()
        messages.add_message(request, messages.INFO, 'Card Created')

    context['form'] = form
    return render(request, 'create_card.html', context)
