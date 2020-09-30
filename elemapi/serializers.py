from rest_framework import serializers
from elemcore import models as emodels

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = emodels.Card
        fields = ('')