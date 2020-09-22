from django.shortcuts import render
from elemcore.models import Card

def ShowHome(request):
    cards = Card.objects.all()
    print("object:", cards)
    for card in cards:
        print(dir(card))
    return render(request,
                  "home.html",
                    {
                    'cards': cards,
                    })
