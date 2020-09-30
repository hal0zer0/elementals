from django.urls import path, include
from rest_framework import routers
from elemapi import views

router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

