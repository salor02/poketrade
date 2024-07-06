from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import *
from .forms import ListingCreateForm, ListingUpdateForm, TransactionCreateForm, TransactionUpdateForm, FeedbackCreateForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotFound 
from .utils import *
from django.db.models import Q, F, Count

# Create your views here.
class ListingsListView(ListView):
    model = Listing
    template_name = "marketplace/listings_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(user = self.kwargs['user_id']).annotate(
            pending_transactions_count=Count('transactions', filter=Q(transactions__accepted=None))
        ).order_by('sold', '-created_at')

        if self.request.user.is_authenticated and self.request.user.id != self.kwargs['user_id']:
            return queryset.filter(published=True)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = get_object_or_404(User, id=self.kwargs['user_id'])
        context['owner'] = owner
        return context
        
class MarketListingListView(ListView):
    model = Listing
    template_name = "marketplace/market.html"

    def search(self):
        search_query = self.request.GET.get('search','').upper()

        res = self.model.objects.none()

        if search_query:
            for param in search_query.split(" "):
                res |= self.model.objects.filter(
                    Q(cards_for_sale__cod=param) |
                    Q(cards_in_exchange__cod=param)
                )

        return res
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search','').upper()
        if search_query:
            search_query = search_query.split(" ")
        context['search_query'] = search_query
        context['form'] = SearchForm
        return context

    def get_queryset(self):

        search_res = self.search()
        if search_res:
            queryset = search_res
        else:
            queryset = self.model.objects

        #recommendation system
        if self.request.user.is_authenticated:
            res = queryset.filter(published=True, sold=False
                ).exclude(user=self.request.user
                ).annotate(
                    cards_in_wishlist=Count('cards_for_sale', filter=Q(cards_for_sale__wishlists__user=self.request.user), distinct=True),
                    cards_in_collection=Count('cards_in_exchange', filter=Q(cards_in_exchange__owners=self.request.user), distinct=True)
                ).annotate(
                    total_score=F('cards_in_wishlist') + F('cards_in_collection')
                ).order_by('-total_score','-published_at')
            
            print("\nRecommendation system result")
            for item in res:
                print(f'[{item.id} - {item.user.username}] Cards in wishlist: {item.cards_in_wishlist} - Cards in collection: {item.cards_in_collection} --> Total score: {item.total_score}')
            print()

            return res
        else:
            return queryset.filter(published=True, sold=False).order_by('-published_at')
    
class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = 'marketplace/listing_create.html'

    def form_valid(self, form):
       form.instance.user = self.request.user
       response = super().form_valid(form)
       return response
    
    def get_success_url(self):
        return reverse_lazy('marketplace:start_selection', kwargs={'listing_id' : self.object.id})
    
class ListingUpdateView(LoginRequiredMixin, UpdateView):
    model = Listing
    form_class = ListingUpdateForm
    template_name = 'marketplace/listing_update.html'
    pk_url_kwarg = 'listing_id'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('marketplace:listings_list', kwargs={'user_id' : self.request.user.id})+'?updated=1'
    
class ListingDetailView(DetailView):
    model = Listing
    template_name = 'marketplace/listing_detail.html'
    pk_url_kwarg = 'listing_id'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(Q(user=self.request.user) | Q(published=True))
        else:
            return self.model.objects.filter(published=True)
        
class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionCreateForm
    template_name = 'marketplace/transaction_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.listing = get_object_or_404(Listing, id=self.kwargs['listing_id'])
        
        if self.request.user.is_authenticated:
            if self.listing.user == self.request.user:
                return HttpResponseNotFound('Non puoi acquistare un tuo articolo')
            elif not self.listing.published:
                return HttpResponseNotFound('Articolo non disponibile per la vendita')
            elif self.listing.sold:
                return HttpResponseNotFound('Articolo venduto')
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listing'] = self.listing
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['listing_id'] = self.kwargs['listing_id']
        return kwargs

    def form_valid(self, form):
        form.instance.listing = get_object_or_404(Listing, id=self.kwargs['listing_id'])
        form.instance.buyer = self.request.user
        response = super().form_valid(form)
        return response
    
    def get_success_url(self):
        return reverse_lazy('marketplace:pending_transaction_list')+'?created=1'
    
class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "marketplace/transaction_list.html"

    def get_queryset(self):
        listing = get_object_or_404(Listing, id=self.kwargs['listing_id'])
        return self.model.objects.filter(Q(accepted=None) | Q(accepted=False), listing=listing).order_by('accepted')
    
class AcceptedTransactionListView(TransactionListView):
    def get_queryset(self):
        return self.model.objects.filter(accepted=True, listing__user=self.request.user)
    
class PurchasedTransactionListView(TransactionListView):
    def get_queryset(self):
        return self.model.objects.filter(accepted=True, buyer=self.request.user)
    
class PendingTransactionListView(TransactionListView):
    def get_queryset(self):
        return self.model.objects.filter(Q(accepted=None) | Q(accepted=False), buyer=self.request.user).order_by('accepted')

    
class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionUpdateForm
    template_name = 'marketplace/transaction_update.html'
    pk_url_kwarg = 'transaction_id'
    
    def get_queryset(self):
        return self.model.objects.filter(accepted=None, listing__user=self.request.user, listing__sold=False)

    def get_success_url(self):
        return reverse_lazy('marketplace:listings_list', kwargs={'user_id' : self.request.user.id})+'?updatedTransaction=1'
    
class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = 'marketplace/transaction_detail.html'
    pk_url_kwarg = 'transaction_id'

    def get_queryset(self):
        return self.model.objects.filter(Q(buyer=self.request.user) | Q(listing__user=self.request.user))
    
class FeedbackUpdateView(LoginRequiredMixin, UpdateView):
    model = Feedback
    form_class = FeedbackCreateForm
    template_name = 'marketplace/feedback_send.html'
    pk_url_kwarg = 'transaction_id'

    def dispatch(self, request, *args, **kwargs):
        self.transaction = get_object_or_404(Transaction, id=self.kwargs['transaction_id'])
        if not self.transaction.buyer == self.request.user and not self.transaction.listing.user == self.request.user:
            return HttpResponseNotFound('Non sei un partecipante di questa transazione')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Feedback, transaction__id=self.kwargs['transaction_id'], user_src=self.request.user)

    def form_valid(self, form):
        form.instance.transaction = self.transaction
        form.instance.user_src =  self.request.user
        form.instance.user_dst = self.transaction.listing.user if self.transaction.buyer == self.request.user else self.transaction.buyer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class FeedbackDetailView(DetailView):
    model = Feedback
    template_name = 'marketplace/feedback_detail.html'
    pk_url_kwarg = 'feedback_id' 

    def get_queryset(self):
        return self.model.objects.filter(rating__isnull=False)
    
class FeedbackUserListView(ListView):
    model = Feedback
    template = 'marketplace/feedback_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user_dst=self.kwargs['user_id'])

@login_required
def end_selection(request):
    if 'listing_id' in request.session:
        listing_id = request.session['listing_id']
    else:
        return HttpResponseBadRequest('Sessione non configurata correttamente')
    
    try:
        if set_selection_mode(request, False):
            return redirect(reverse_lazy('marketplace:listing_update', kwargs={'listing_id' : listing_id}))
        else:
            return HttpResponseBadRequest('Sessione non configurata correttamente')
    except Http404:
        return HttpResponseNotFound("L'annuncio che si sta tentando di modificare non esiste")

    
@login_required
def start_selection(request, listing_id):
    try:
        if set_selection_mode(request, True, 'for_sale', listing_id):
            return redirect(reverse_lazy('collection:collection', kwargs={'user_id' : request.user.id}))
        else:
            return HttpResponseBadRequest('Sessione non configurata correttamente')
    except Http404:
        return HttpResponseNotFound("L'annuncio che si sta tentando di modificare non esiste")

@login_required
def start_in_exchange_selection(request):
    if not 'listing_id' in request.session:
        return HttpResponseBadRequest('Sessione non configurata correttamente')
    
    try:
        if set_selection_mode(request, True, 'in_exchange', request.session['listing_id']):
            return redirect(reverse_lazy('collection:game_list'))
        else:
            return HttpResponseBadRequest('Sessione non configurata correttamente')
    except Http404:
        return HttpResponseNotFound("L'annuncio che si sta tentando di modificare non esiste")

