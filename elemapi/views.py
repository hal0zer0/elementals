from rest_framework import viewsets
from .serializers import CardSerializer
from elemcore import models as emodels

class CardViewSet(viewsets.ModelViewSet):
    queryset = emodels.Construct.objects.all().order_by('name') | emodels.Action.objects.all()
    serializer_class = CardSerializer
