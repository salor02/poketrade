from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Hidden
from .models import *
from .urls import *
from api.urls import *

#non serve
class WishlistCrispyForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_id = 'addNewWishlist'

    class Meta:
        model = Wishlist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome della nuova wishlist'}),
        }
        labels = {
            'name':''
        }

    helper.layout = Layout(
        Hidden('action', 'add'),
        Row(
            Column('name', css_class='form-group col-md-6 mb-0'),
            Column(Submit('submit', 'Aggiungi', css_class='btn btn-primary form-group col-md-6'))
        )
    )