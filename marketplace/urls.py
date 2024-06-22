from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'marketplace'

urlpatterns = [
    path('listings/<int:user_id>/', ListingsListView.as_view(extra_context={'title':'Listings'}), name='listings_list'),
    path('listing/create/', ListingCreateView.as_view(extra_context={'title':'Creazione annuncio'}), name='listing_create'),
    path('listing/<int:listing_id>/update/', ListingUpdateView.as_view(extra_context={'title':'Modifica annuncio'}), name='listing_update'),
    path('listing/<int:listing_id>/detail/', ListingDetailView.as_view(extra_context={'title':'Visualizza annuncio'}), name='listing_detail'),

    path('market/', MarketListingListView.as_view(extra_context={'title':'Market'}), name='market'),

    path('end-selection/', end_selection, name = 'end_selection'),
    path('start-selection/<int:listing_id>/', start_selection, name = 'start_selection'),
    path('in-exchange-selection/', start_in_exchange_selection, name = 'start_in_exchange_selection')
]

