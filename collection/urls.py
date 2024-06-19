from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

app_name = 'collection'

urlpatterns = [
    path('games/', GameListView.as_view(extra_context={'title': 'Games'}), name = 'game_list'),
    path('game/<int:game_id>/sets', SetListView.as_view(extra_context={'title':'Set list'}), name = 'set_list'),
    path('game/<int:game_id>/set/<int:set_id>/cards', SetCardView.as_view(extra_context={'title':'Card list'}), name = 'card_list'),
    path('game/<int:game_id>/set/<int:set_id>/card/<int:card_id>/detail', CardDetailView.as_view(), name = 'card_detail'),

    path('wishlists/', WishlistListView.as_view(extra_context={'title':'My wishlists'}), name = 'wishlist_list'),
    path('wishlist/<int:wishlist_id>/detail', WishlistView.as_view(extra_context={'title':'Wishlist'}), name = 'wishlist_detail'),
    
    path('collection/<int:user_id>/detail', CollectionView.as_view(extra_context={'title':'Collection'}), name = 'collection'),

    #da migliorare, forse creando API
    path('manage/', collection_manage, name='collection_manage'),
]