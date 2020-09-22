from django.shortcuts import render
from elemcore.models import Card

def ShowHome(request):
    cards = Card.objects.all()
    return render(request,
                  "home.html",
                    {
                    'cards': cards,
                    })
