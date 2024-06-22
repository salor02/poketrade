from django.db import models
from django.contrib.auth.models import User
from collection.models import Card
from django.core.exceptions import ValidationError

# Create your models here.

class Listing(models.Model):

    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField(default=False)

    cards_for_sale = models.ManyToManyField(Card, related_name='listings_for_sale', blank=True)
    cards_in_exchange = models.ManyToManyField(Card, related_name='listings_in_exchange', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')

    def clean(self):
        super().clean()
        if self.price and self.price < 0:
            raise ValidationError('Il prezzo non può essere negativo')
