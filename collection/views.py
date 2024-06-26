from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, Http404
from .utils import get_cards_by_set
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from marketplace.models import Listing

# Create your views here.

class GameListView(ListView):
    model = Game
    template_name = "collection/game_list.html"

class SetListView(ListView):
    model = Set
    template_name = "collection/set_list.html"

    def get_queryset(self):
        game_id = self.kwargs['game_id']
        return self.model.objects.filter(game_id=game_id)
    
class CardDetailView(DetailView):
    model = Card
    template_name = "collection/card_detail.html"
    pk_url_kwarg = 'card_id'

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "collection/wishlist_list.html"

    def get_queryset(self):
        return self.model.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WishlistCrispyForm
        return context

class CardListView(TemplateView):
    template_name = 'collection/card_list.html'

    def get_owned_and_wishlists(self):
        owned = []
        wishlists = []
        if(self.request.user.is_authenticated):
            owned = Card.objects.filter(owners=self.request.user)
            wishlists = Wishlist.objects.filter(user=self.request.user)
        return owned, wishlists
    
    def get_listed(self):
        listed = []
        if self.request.user.is_authenticated and 'selection' in self.request.session:
            listing_id = self.request.session['listing_id']
            if listing_id:
                try:
                    if self.request.session['selection_dest'] == 'for_sale':
                        listed = Listing.objects.get(pk=listing_id, user=self.request.user).cards_for_sale.all()
                    elif self.request.session['selection_dest'] == 'in_exchange':
                        listed = Listing.objects.get(pk=listing_id, user=self.request.user).cards_in_exchange.all()
                except Listing.DoesNotExist:
                    return []
        return listed
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        listed = self.get_listed()
        owned, wishlists = self.get_owned_and_wishlists()
        cards_by_set = get_cards_by_set(self.get_queryset())

        context['owned'] = owned
        context['wishlists'] = wishlists
        context['cards_by_set'] = cards_by_set
        context['listed'] = listed
        return context

class CollectionView(CardListView):
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        return user.owned_cards.all()

class WishlistView(CardListView):
    def get_queryset(self):
        wishlist_id = self.kwargs.get('wishlist_id')
        wishlist = get_object_or_404(Wishlist, pk=wishlist_id)
        return wishlist.cards.all()
    
class SetCardView(CardListView):
    def get_queryset(self):
        set_id = self.kwargs.get('set_id')
        set = get_object_or_404(Set, pk=set_id)
        return set.cards.all()

@login_required
@require_POST
def collection_manage(request):

    wishlist = None
    if 'wishlist_id' in request.POST:
        try:
            wishlist = Wishlist.objects.get(pk=request.POST['wishlist_id'], user = request.user)
        except Wishlist.DoesNotExist:
            return HttpResponseBadRequest(f"Non esiste nessuna wishlist con ID {request.POST['wishlist_id']} per l'utente attuale")
        
    if 'card_id' in request.POST and 'action' in request.POST:
        try:
            card = Card.objects.get(pk=request.POST['card_id'])
        except Card.DoesNotExist:
            return HttpResponseBadRequest('La carta con ID fornito non esiste')
        
        if request.POST['action'] == 'add':
            if wishlist:
                wishlist.cards.add(card)
                return JsonResponse({'success':f'Carta aggiunta alla wishlist {wishlist.name}'})
            else:
                card.owners.add(request.user)
                return JsonResponse({'success':'Carta correttamente aggiunta alla collezione'})
        elif request.POST['action'] == 'remove':
            if wishlist:
                wishlist.cards.remove(card)
                return JsonResponse({'success':f'Carta rimossa dalla wishlist {wishlist.name}'})
            else:
                card.owners.remove(request.user)
                return JsonResponse({'success':'Card correttamente rimossa dalla collezione'})
        else:
            return HttpResponseBadRequest('Questa azione non è valida')
    return HttpResponseBadRequest('Il parametro action o card_id risultano mancanti')

    