from django.db import models
from django.contrib.auth.models import User
from collection.models import Card
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Listing(models.Model):

    description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    cards_for_sale = models.ManyToManyField(Card, related_name='listings_for_sale', blank=True)
    cards_in_exchange = models.ManyToManyField(Card, related_name='listings_in_exchange', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError('Il prezzo non può essere negativo')
        
    class Meta:
        ordering = ['-created_at']
        
class Transaction(models.Model):
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accepted = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_transactions')

    proposed_cards = models.ManyToManyField(Card, related_name='proposed_transactions', blank=True)
    wanted_cards = models.ManyToManyField(Card, related_name='wanted_transactions', blank=True)

    def clean(self):
        super().clean()
        if self.proposed_price < 0:
            raise ValidationError('Il prezzo non può essere negativo')
    
    class Meta:
        ordering = ['-created_at']

class Feedback(models.Model):
    comment = models.CharField(max_length=200, blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Valuta da 1 a 10"
    )

    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='feedbacks')
    user_src = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedbacks')
    user_dst = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedbacks')
        
@receiver(post_save, sender=Transaction)
def update_listing_sold_out_status(sender, instance, **kwargs):
    if instance.accepted:
        listing = instance.listing
        listing.sold = True
        listing.save()

        other_transactions = listing.transactions.exclude(id=instance.id)
        other_transactions.update(accepted=False)

        feedback_from_buyer = Feedback(
            transaction = instance,
            user_src = instance.buyer,
            user_dst = listing.user
        )
        feedback_from_buyer.save()

        feedback_from_seller = Feedback(
            transaction = instance,
            user_src = listing.user,
            user_dst = instance.buyer
        )
        feedback_from_seller.save()
