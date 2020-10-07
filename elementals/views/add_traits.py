from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from elemcore import models as emodels
from elemcore.forms import TraitsForm


def show(request, construct_id):
    construct = get_object_or_404(emodels.Construct, id=construct_id)
    traits_form = TraitsForm(request.POST or None)
    if traits_form.is_valid():
        print("got a valid form")
        data = traits_form.cleaned_data
        ids = [trait.id for trait in data['traits']]  # I just love list comprehensions!
        construct.traits.set(ids)
        construct.save()
        messages.add_message(request, messages.INFO, "Traits saved!")
        #return redirect("traits", construct_id=construct_id)

    return render(request, 'add_traits.html', {'traits_form': traits_form})
