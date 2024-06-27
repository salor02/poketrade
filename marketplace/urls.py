from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'marketplace'

urlpatterns = [
    path('listings/<int:user_id>/', ListingsListView.as_view(extra_context={'title':'Lista annunci'}), name='listings_list'),
    path('listing/create/', ListingCreateView.as_view(extra_context={'title':'Creazione annuncio'}), name='listing_create'),
    path('listing/<int:listing_id>/update/', ListingUpdateView.as_view(extra_context={'title':'Modifica annuncio'}), name='listing_update'),
    path('listing/<int:listing_id>/detail/', ListingDetailView.as_view(extra_context={'title':'Visualizza annuncio'}), name='listing_detail'),

    path('market/', MarketListingListView.as_view(extra_context={'title':'Market'}), name='market'),
    path('listing/<int:listing_id>/buy/', TransactionCreateView.as_view(extra_context={'title':'Acquisto'}), name='transaction_create'),
    path('listing/<int:listing_id>/transactions/', TransactionListView.as_view(extra_context={'title':'Lista proposte'}), name='transaction_list'),
    path('transaction/<int:transaction_id>/update/', TransactionUpdateView.as_view(extra_context={'title':'Valuta proposta'}), name='transaction_update'),
    path('transaction/<int:transaction_id>/detail/', TransactionDetailView.as_view(extra_context={'title':'Visualizza proposta'}), name='transaction_detail'),
    path('transactions/accepted/', AcceptedTransactionListView.as_view(extra_context={'title':'Vendite'}), name='accepted_transaction_list'),
    path('transactions/pending/', PendingTransactionListView.as_view(extra_context={'title':'Proposte inviate'}), name='pending_transaction_list'),
    path('transactions/purchases/', PurchasedTransactionListView.as_view(extra_context={'title':'Acquisti'}), name='purchased_transaction_list'),

    path('feedback/<int:transaction_id>/send/', FeedbackUpdateView.as_view(extra_context={'title':'Invia feedback'}), name='feedback_send'),
    path('feedback/<int:feedback_id>/detail/', FeedbackDetailView.as_view(extra_context={'title':'Visualizza feedback'}), name='feedback_detail'),
    path('feedback/<int:user_id>/list/', FeedbackUserListView.as_view(extra_context={'title':'Lista feedback utente'}), name='feedback_list'),

    path('end-selection/', end_selection, name = 'end_selection'),
    path('start-selection/<int:listing_id>/', start_selection, name = 'start_selection'),
    path('in-exchange-selection/', start_in_exchange_selection, name = 'start_in_exchange_selection')
]

