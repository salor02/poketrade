from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Listing
from .forms import ListingCrispyForm, ListingUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotFound 
from .utils import *
from django.db.models import Q

# Create your views here.
class ListingsListView(ListView):
    model = Listing
    template_name = "marketplace/listings_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user = self.kwargs['user_id'])
        
class MarketListingListView(ListView):
    model = Listing
    template_name = "marketplace/market.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(published=True).exclude(user=self.request.user)
        else:
            return self.model.objects.filter(published=True)
    
class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingCrispyForm
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
        return reverse_lazy('marketplace:listings_list', kwargs={'user_id' : self.request.user.id})
    
class ListingDetailView(DetailView):
    model = Listing
    template_name = 'marketplace/listing_detail.html'
    pk_url_kwarg = 'listing_id'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(Q(user=self.request.user) | Q(published=True))
        else:
            return self.model.objects.filter(published=True)

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

