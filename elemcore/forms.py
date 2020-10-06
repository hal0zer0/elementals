from django.forms import ModelForm
from elemcore import models as emodels

class ConstructForm(ModelForm):
    class Meta:
        model = emodels.Construct
        fields = ['name', 'attack', 'defense']