from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from elemcore import models as emodels


def show(request, username):
    user = get_object_or_404(User, username=username)
    my_cards = emodels.Card.objects.filter(user=user)
    my_decks = emodels.Deck.objects.filter(owner=user)
    print("My Cards:", my_cards)
    print(user)
    return render(request, 'profile.html', {'user': user,
                                            'my_cards': my_cards})
