from rest_framework import serializers
from elemcore import models as emodels
from django.contrib.auth.models import User

class RaritySerializer(serializers.ModelSerializer):
    class Meta:
        model = emodels.Rarity
        fields = ('level', 'label',)

class CardSubtypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = emodels.CardSubtype
        fields = ('name',)


class CardSerializer(serializers.HyperlinkedModelSerializer):
    rarity = RaritySerializer()
    subtype = CardSubtypeSerializer()
    class Meta:
        model = emodels.Card
        if hasattr(model, 'construct'):
            fields = ['url', 'id', 'name', 'card_type', 'rarity', 'subtype', 'attack_value', 'defense_value']
        depth = 1




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
