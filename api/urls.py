from django.urls import path
from rest_framework import routers
from .views import *

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'wishlists', WishlistViewSet, basename='wishlists')
router.register(r'listings', ListingViewSet, basename='listings')

urlpatterns = router.urls

#urlpatterns+=[path('listings/<int:pk>/add-cards/', AddCardToListingView.as_view(), name='add_cards_to_listing'),]