from rest_framework import serializers
from collection.models import Wishlist, Card

class CardSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    cards = CardSerializer(read_only = True, many = True)
    
    class Meta:
        model = Wishlist
        fields = '__all__'