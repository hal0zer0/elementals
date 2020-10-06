from django.shortcuts import render
from elemcore import models as emodels
from elemcore import forms

def show(request):
    form = forms.ConstructForm()
    return render(request, 'create_card.html', {'form': form})
