from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import *
from collection.models import *
from .forms import TransactionCreateForm
from marketplace.utils import set_selection_mode, clear_session

class TransactionCreateFormTests(TestCase):
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

    def test_form_invalid_no_proposed_cards(self):
        form_data = {
            'proposed_price': 50,
            'wanted_cards': [self.card2.id]
        }
        form = TransactionCreateForm(data=form_data, listing_id=self.listing.id)
        self.assertTrue(form.is_valid())

    def test_listing_not_found(self):
        form_data = {
            'proposed_price': 50,
            'proposed_cards': [self.card1.id],
            'wanted_cards': [self.card2.id]
        }

        with self.assertRaises(Http404):
            form = TransactionCreateForm(data=form_data, listing_id=99999999)

    def test_listing_is_none(self):
        form_data = {
            'proposed_price': 50,
            'proposed_cards': [self.card1.id],
            'wanted_cards': [self.card2.id]
        }

        with self.assertRaises(Http404):
            form = TransactionCreateForm(data=form_data, listing_id=None)

    def test_form_proposed_cards_queryset(self):
        form = TransactionCreateForm(listing_id=self.listing.id)
        self.assertEqual(list(form.fields['proposed_cards'].queryset), list(self.listing.cards_in_exchange.all()))
    
    def test_form_wanted_cards_queryset(self):
        form = TransactionCreateForm(listing_id=self.listing.id)
        self.assertEqual(list(form.fields['wanted_cards'].queryset), list(self.listing.cards_for_sale.all()))

class SetSelectionModeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.listing = Listing.objects.create(user=self.user, description='Test Listing', price=345)
        self.factory = RequestFactory()

    def test_user_not_authenticated(self):
        request = self.factory.get('/')
        request.session = {}
        response = set_selection_mode(request, True, 'destination', self.listing.id)

        self.assertFalse(response)

    def test_missing_session_keys(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {'selection_dest': 'old_dest', 'listing_id': 123}
        response = set_selection_mode(request, True, 'destination', self.listing.id)

        self.assertTrue(response)
        self.assertTrue(request.session['selection'])
        self.assertEqual(request.session['selection_dest'], 'destination')
        self.assertEqual(request.session['listing_id'], self.listing.id)

    def test_status_false(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {'selection_dest': 'old_dest', 'listing_id': 123, 'selection': True}
        response = set_selection_mode(request, False, 'destination', self.listing.id)

        self.assertTrue(response)
        self.assertIsNone(request.session['selection_dest'])
        self.assertIsNone(request.session['listing_id'])
        self.assertFalse(request.session['selection'])

    def test_missing_parameters(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        response = set_selection_mode(request, True)

        self.assertFalse(response)
        self.assertIsNone(request.session['selection_dest'])
        self.assertIsNone(request.session['listing_id'])
        self.assertFalse(request.session['selection'])

    def test_successful_set_selection_mode(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        response = set_selection_mode(request, True, 'destination', self.listing.id)

        self.assertTrue(response)
        self.assertTrue(request.session['selection'])
        self.assertEqual(request.session['selection_dest'], 'destination')
        self.assertEqual(request.session['listing_id'], self.listing.id)

    def test_listing_not_found(self):
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        
        with self.assertRaises(Http404):
            response = set_selection_mode(request, True, 'destination', 9999999999) 
