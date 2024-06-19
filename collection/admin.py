from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Set)
admin.site.register(Card)
admin.site.register(Wishlist)
admin.site.register(Session)