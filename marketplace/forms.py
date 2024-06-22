from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Hidden
from .models import *
from .urls import *
from api.urls import *

class ListingCrispyForm(forms.ModelForm):

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