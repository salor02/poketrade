from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest
from .models import *

class CollectionManageViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Creazione dei dati di test
        self.game = Game.objects.create(name='Test Game', img_url='test_game.png')
        self.set = Set.objects.create(name='Test Set', cod='TS01', img_url='test_set.png', game=self.game)
        self.card = Card.objects.create(name='Test Card', cod='TC01', img_url='test_card.png', move1='Move 1', move2='Move 2', description='Description', set=self.set)
        self.wishlist = Wishlist.objects.create(name='Test Wishlist', user=self.user)
        
        self.url = reverse('collection:collection_manage')

    def test_add_card_to_collection(self):
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'add'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': 'Carta correttamente aggiunta alla collezione'})
        self.assertIn(self.card, self.user.owned_cards.all())

    def test_remove_card_from_collection(self):
        self.user.owned_cards.add(self.card)
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'remove'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': 'Card correttamente rimossa dalla collezione'})
        self.assertNotIn(self.card, self.user.owned_cards.all())

    def test_add_card_to_wishlist(self):
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'add', 'wishlist_id': self.wishlist.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': f'Carta aggiunta alla wishlist {self.wishlist.name}'})
        self.assertIn(self.card, self.wishlist.cards.all())

    def test_remove_card_from_wishlist(self):
        self.wishlist.cards.add(self.card)
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'remove', 'wishlist_id': self.wishlist.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': f'Carta rimossa dalla wishlist {self.wishlist.name}'})
        self.assertNotIn(self.card, self.wishlist.cards.all())

    def test_invalid_action(self):
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'invalid_action'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Questa azione non è valida')

    def test_missing_action(self):
        response = self.client.post(self.url, {'card_id': self.card.id})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Il parametro action o card_id risultano mancanti')

    def test_missing_card_id(self):
        response = self.client.post(self.url, {'action': 'add'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'Il parametro action o card_id risultano mancanti')

    def test_non_existent_card(self):
        response = self.client.post(self.url, {'card_id': 999999999999, 'action': 'add'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), 'La carta con ID fornito non esiste')

    def test_non_existent_wishlist(self):
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'add', 'wishlist_id': 999})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode(), f"Non esiste nessuna wishlist con ID 999 per l'utente attuale")

    def test_not_authenticated(self):
        self.client.logout()
        response = self.client.post(self.url, {'card_id': self.card.id, 'action': 'add'})
        self.assertEqual(response.status_code, 302)  # Redirect to login


