from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from elemcore import models as emodels
from elemcore.forms import AbilitiesForm


def show(request, construct_id):
    """
    construct = get_object_or_404(emodels.Construct, id=construct_id)
    if request.method == "POST":
        form = request.POST
        #print(form.items())
        for item in form.items():
            print(item)
    rlevel = construct.rarity.level
    rlabel = construct.rarity.label
    abilities = emodels.Ability.objects.filter(rarity__lte=rlevel)
    traits = emodels.Trait.objects.all()

    return render(request, 'add_abilities.html', {'abilities': abilities,
                                                  'traits': traits,
                                                  'rarity': rlabel})"""
    form = AbilitiesForm(request.POST or None)
    return render(request, 'add_abilities.html', {'form': form})