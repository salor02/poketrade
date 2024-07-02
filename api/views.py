from rest_framework import viewsets
from collection.models import Wishlist
from marketplace.models import Listing
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponseBadRequest, JsonResponse

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.sold:
            return HttpResponseBadRequest('Non è possibile eliminare un annuncio già venduto')
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post','delete'], url_path='add-remove-cards')
    def add_remove_card(self, request, pk=None):
        listing = self.get_object()
        card_id = request.data.get('card_id')
        selection_dest = request.data.get('selection_dest')

        if not selection_dest:
            return HttpResponseBadRequest('Non è stata specificata nessuna destinazione per la selezione')

        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist:
            return HttpResponseBadRequest('La carta richiesta non esiste')
        
        if request.method == 'POST':
            if selection_dest == 'for_sale':
                listing.cards_for_sale.add(card)
                response = "Carta aggiunta all'offerta"
            elif selection_dest == 'in_exchange':
                listing.cards_in_exchange.add(card)
                response = "Carta aggiunta alla richiesta di scambio"
            
        elif request.method == 'DELETE':
            if selection_dest == 'for_sale':
                listing.cards_for_sale.remove(card)
                response = "Carta rimossa dall'offerta"
            elif selection_dest == 'in_exchange':
                listing.cards_in_exchange.remove(card)
                response = "Carta rimossa dalla richiesta di scambio"
        
        listing.save()
        return JsonResponse({'status': response})