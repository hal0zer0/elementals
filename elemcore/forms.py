from django import forms
from elemcore import models as emodels

class ConstructForm(forms.ModelForm):
    subtype = forms.CharField(max_length=16)

    def save(self, commit=True):
        subtype_name = self.cleaned_data['subtype']
        subtype = emodels.CardSubtype.objects.get_or_create(name=subtype_name)[0]
        self.instance.subtype = subtype
        return super(ConstructForm, self).save(commit)

    class Meta:
        model = emodels.Construct
        fields = ['name', 'attack', 'defense', 'picture', 'flavor_text', 'rarity', 'public', 'user'] # User is hidden
        widgets = {'user': forms.HiddenInput()}