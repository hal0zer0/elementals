from rest_framework import viewsets
from .serializers import CardSerializer, RaritySerializer, CardSubtypeSerializer, UserSerializer
from elemcore import models as emodels
from django.contrib.auth.models import User

class CardViewSet(viewsets.ModelViewSet):
    queryset = emodels.Card.objects.filter(public=True)
    serializer_class = CardSerializer

class RarityViewSet(viewsets.ModelViewSet):
    queryset = emodels.Rarity.objects.all()
    serializer_class = RaritySerializer

class CardSubtypeViewSet(viewsets.ModelViewSet):
    queryset = emodels.CardSubtype.objects.all()
    serializer_class = CardSubtypeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
