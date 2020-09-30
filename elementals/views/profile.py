from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


def show(request, username):
    user = get_object_or_404(User, username=username)
    print(user)
    return render(request, 'profile.html', {user: user})
