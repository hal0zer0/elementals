from django.urls import path, include
from rest_framework import routers
from elemapi import views

router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet)
router.register(r'rarity', views.RarityViewSet)
router.register(r'cardsubtype', views.CardSubtypeViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

