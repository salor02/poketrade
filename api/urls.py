from django.urls import path
from rest_framework import routers
from .views import WishlistViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'wishlists', WishlistViewSet, basename='wishlists')

urlpatterns = router.urls