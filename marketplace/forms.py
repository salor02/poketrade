from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Hidden, Fieldset, Field, Div, ButtonHolder
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import *
#from .urls import *
from api.urls import *

class ListingCreateForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Seleziona carte'))

    class Meta:
        model = Listing
        fields = ['description', 'price']

class ListingUpdateForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Salva annuncio'))

    class Meta:
        model = Listing
        fields = ['description', 'price', 'published']

class TransactionUpdateForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Invia'))

    accepted = forms.TypedChoiceField(
        choices=((True, 'Sì'), (False, 'No')),
        widget=forms.RadioSelect,
        required=True,
        initial=False
    )

    class Meta:
        model = Transaction
        fields = ['accepted']

class TransactionCreateForm(forms.ModelForm):
    proposed_cards = forms.ModelMultipleChoiceField(
        queryset=Card.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    wanted_cards = forms.ModelMultipleChoiceField(
        queryset=Card.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Transaction
        fields = ['proposed_price', 'proposed_cards', 'wanted_cards']
    
    def __init__(self, *args, **kwargs):
        listing_id = kwargs.pop('listing_id', None)
        super().__init__(*args, **kwargs)
        
        if listing_id is not None:
            self.fields['proposed_cards'].queryset = get_object_or_404(Listing, id=listing_id).cards_in_exchange.all()
            self.fields['wanted_cards'].queryset = get_object_or_404(Listing, id=listing_id).cards_for_sale.all()
        else:
            raise Http404

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.layout = Layout(
            'proposed_price',
            Fieldset('Carte offerte in scambio', 'proposed_cards', template='marketplace/card_image_select.html'),
            Fieldset('Carte da acquistare', 'wanted_cards', template='marketplace/card_image_select.html'),
            Submit('submit', 'Invio')
        )
    
class FeedbackCreateForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Invia'))

    class Meta:
        model = Feedback
        fields = ['rating', 'comment']

    rating = forms.DecimalField(
        required=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Valuta da 1 a 10"
    )

class SearchForm(forms.Form):
    search = forms.CharField(
        label=False,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Inserisci codice ESATTO della carta da cercare (oppure più codici separati da spazio)',
            'class': 'form-control'
        })
    )

    helper = FormHelper()
    helper.form_method = 'get'
    helper.layout = Layout(
        Div(
            Field('search', wrapper_class='col-sm-10'),
            Div(
                Submit('submit', 'Cerca', css_class='btn-primary'), 
                css_class='d-grid col-2'
            ),
            css_class='row mb-4'
        )
    )