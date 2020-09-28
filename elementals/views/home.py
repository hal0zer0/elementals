from django.shortcuts import render
from elemcore.models import Card, Deck

def ShowHome(request):
    cards = Card.objects.all()
    decks = Deck.objects.all()
    return render(request,
                  "home.html",
                    {
                    'cards': cards,
                    'decks': decks,
                    })
