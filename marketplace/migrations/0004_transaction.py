# Generated by Django 5.0.6 on 2024-06-23 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_alter_wishlist_cards'),
        ('marketplace', '0003_alter_listing_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('accepted', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_transactions', to=settings.AUTH_USER_MODEL)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='marketplace.listing')),
                ('proposed_cards', models.ManyToManyField(blank=True, related_name='proposed_transactions', to='collection.card')),
                ('wanted_cards', models.ManyToManyField(blank=True, related_name='wanted_transactions', to='collection.card')),
            ],
        ),
    ]
