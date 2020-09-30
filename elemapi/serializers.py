from rest_framework import serializers
from elemcore import models as emodels
from django.contrib.auth.models import User

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = emodels.Card
        fields = ['id', 'name', 'card_type', 'rarity', 'subtype']
        depth = 1

class RaritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = emodels.Rarity
        fields = ('label',)

class CardSubtypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = emodels.CardSubtype
        fields = ('name',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
