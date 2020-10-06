from django import forms
from elemcore import models as emodels
from django.template.defaultfilters import safe

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

class AbilitiesForm(forms.Form):
    abilities = forms.ModelMultipleChoiceField(
                      queryset=emodels.Ability.objects.all(),
                      widget=forms.CheckboxSelectMultiple,
    )
    class Meta:
        model = emodels.Ability
        fields = ('text',)
