from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import *
from .forms import *
from collection.models import Set
from collection.utils import get_cards_by_set
from django.db.models import Count

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("user:login")

class UserDetailView(DetailView):
    model = User
    template_name = "user/account.html"
    pk_url_kwarg = 'user_id'

    sets = Set.objects.annotate(cards_num=Count('cards'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.get(id=user_id)

        received_ratings = [feedback.rating for feedback in user.received_feedbacks.filter(rating__isnull=False)]

        if len(received_ratings) > 0:
            avg_rating = sum(received_ratings) / len(received_ratings)
        else:
            avg_rating = None
        
        owned_cards = user.owned_cards.all()
        cards_by_set = get_cards_by_set(owned_cards)

        for set, cards in cards_by_set.items():
            num_set_cards = self.sets.get(id=set.id).cards_num
            cards_by_set[set] = {'num_owned_cards': len(cards), 'num_set_cards': num_set_cards, 'completing_score': (len(cards)/num_set_cards)*100}

        context['cards_by_set'] = cards_by_set
        context['title'] = 'Account'
        context['avg_rating'] = avg_rating
        return context
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'user/account_edit.html'

    def get_object(self, queryset=None):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    def get_success_url(self):
        return reverse_lazy('user:account_detail', kwargs={'user_id' : self.request.user.id})+'?updated=1'
