from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from elemcore import models as emodels
from elemcore.forms import AbilitiesForm


def show(request, construct_id):
    construct = get_object_or_404(emodels.Construct, id=construct_id)
    rlevel = construct.rarity.level
    rlabel = construct.rarity.label

    abilities_form = AbilitiesForm(request.POST or None, rarity=rlevel)

    if abilities_form.is_valid():
        data = abilities_form.cleaned_data
        ids = [ability.id for ability in data['abilities']] # I just love list comprehensions!
        construct.abilities.set(ids)
        construct.save()
        messages.add_message(request, messages.INFO, "Abilities and traits saved!")
        return redirect("traits", construct_id=construct_id)
    return render(request, 'add_abilities.html', {
                                                  'form': abilities_form,
                                                  'rarity': rlabel,
                                                  'construct': construct})