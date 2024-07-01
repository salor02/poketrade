from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import *
from collection.models import *
from .forms import TransactionCreateForm

"""class TransactionCreateFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user_other = User.objects.create_user(username='otheruser', password='otherpass')
        
        self.game = Game.objects.create(name='Test Game', img_url='test_game.png')
        self.set = Set.objects.create(name='Test Set', cod='TS01', release_date='2023-01-01', img_url='test_set.png', game=self.game)
        
        self.card1 = Card.objects.create(name='Test Card 1', cod='TC01', img_url='test_card1.png', move1='Move 1', description='Description', set=self.set)
        self.card2 = Card.objects.create(name='Test Card 2', cod='TC02', img_url='test_card2.png', move1='Move 2', description='Description', set=self.set)
        
        self.listing = Listing.objects.create(user=self.user_other, price=100.0, published=True, sold=False)
        self.listing.cards_in_exchange.add(self.card1)
        self.listing.cards_for_sale.add(self.card2)

    def test_form_valid(self):
        form_data = {
            'proposed_price': 50,
            'proposed_cards': [self.card1.id],
            'wanted_cards': [self.card2.id]
        }
        form = TransactionCreateForm(data=form_data, listing_id=self.listing.id)
        self.assertTrue(form.is_valid())
    
    def test_form_invalid_no_proposed_price(self):
        form_data = {
            'proposed_cards': [self.card1.id],
            'wanted_cards': [self.card2.id]
        }
        form = TransactionCreateForm(data=form_data, listing_id=self.listing.id)
        self.assertFalse(form.is_valid())
    
    def test_form_invalid_no_wanted_cards(self):
        form_data = {
            'proposed_price': 50,
            'proposed_cards': [self.card1.id]
        }
        form = TransactionCreateForm(data=form_data, listing_id=self.listing.id)
        self.assertFalse(form.is_valid())

    def test_form_proposed_cards_queryset(self):
        form = TransactionCreateForm(listing_id=self.listing.id)
        self.assertEqual(list(form.fields['proposed_cards'].queryset), list(self.listing.cards_in_exchange.all()))
    
    def test_form_wanted_cards_queryset(self):
        form = TransactionCreateForm(listing_id=self.listing.id)
        self.assertEqual(list(form.fields['wanted_cards'].queryset), list(self.listing.cards_for_sale.all()))
"""

from django.test import TestCase, Client
from marketplace.utils import set_selection_mode, clear_session

class SelectionModeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.listing = Listing.objects.create(user=self.user, description='Test Listing', price=100)
        self.client.login(username='testuser', password='testpassword')

    def test_set_selection_mode_authenticated(self):
        session = self.client.session
        response = set_selection_mode(self.client, True, 'for_sale', self.listing.id)
        self.assertTrue(response)
        self.assertTrue(session['selection'])
        self.assertEqual(session['selection_dest'], 'for_sale')
        self.assertEqual(session['listing_id'], self.listing.id)

    def test_set_selection_mode_unauthenticated(self):
        self.client.logout()
        response = set_selection_mode(self.client, True, 'for_sale', self.listing.id)
        self.assertFalse(response)

    def test_set_selection_mode_clear_session(self):
        session = self.client.session
        response = set_selection_mode(self.client, False)
        self.assertTrue(response)
        self.assertFalse(session['selection'])
        self.assertIsNone(session['selection_dest'])
        self.assertIsNone(session['listing_id'])

    def test_set_selection_mode_missing_params(self):
        session = self.client.session
        response = set_selection_mode(self.client, True)
        self.assertFalse(response)
        self.assertFalse(session['selection'])
        self.assertIsNone(session['selection_dest'])
        self.assertIsNone(session['listing_id'])

    def test_clear_session(self):
        session = self.client.session
        session['selection'] = True
        session['selection_dest'] = 'for_sale'
        session['listing_id'] = self.listing.id
        clear_session(session)
        self.assertFalse(session['selection'])
        self.assertIsNone(session['selection_dest'])
        self.assertIsNone(session['listing_id'])


