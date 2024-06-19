from django import forms
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Hidden
from .models import *
from .urls import *

class ProfileUpdateForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Aggiorna'))

    class Meta:
        model = Profile
        fields = ['bio','phone_number','profile_pic']