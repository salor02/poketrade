from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=30)
    img_url = models.CharField(max_length=200)

class Set(models.Model):
    name = models.CharField(max_length=30)
    cod = models.CharField(max_length=10)
    img_url = models.CharField(max_length=200)

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sets')

class Card(models.Model):
    name = models.CharField(max_length=30)
    cod = models.CharField(max_length=10)
    img_url = models.CharField(max_length=200)

    move1 = models.CharField(max_length=30)
    move2 = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=200)

    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='cards')
    owners = models.ManyToManyField(User, related_name='owned_cards')

class Wishlist(models.Model):
    name = models.CharField(max_length=30)

    cards = models.ManyToManyField(Card, related_name='wishlists')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')




