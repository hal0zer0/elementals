"""elementals URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from elementals.views import home, profile, create_construct, add_abilities, add_traits
from elemapi import urls as apiurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(apiurls)),
    path('', home.ShowHome, name="home"),
    path('users/<username>/', profile.show, name="profile"),
    path('create/abilities/<int:construct_id>', add_abilities.show, name="abilities"),
    path('create/traits/<int:construct_id>', add_traits.show, name="traits"),
    path('create/', create_construct.show, name="create_card")
]
