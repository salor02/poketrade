# Generated by Django 5.0.6 on 2024-06-20 12:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collection', '0005_alter_wishlist_cards'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('condition', models.CharField(choices=[('PO', 'Poor'), ('PL', 'Played'), ('LP', 'Light Played'), ('GD', 'Good'), ('EX', 'Excellent'), ('NM', 'Near Mint'), ('MT', 'Mint')], max_length=2)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('published', models.BooleanField(default=False)),
                ('cards_for_sale', models.ManyToManyField(blank=True, related_name='listings_for_sale', to='collection.card')),
                ('cards_in_exchange', models.ManyToManyField(blank=True, related_name='listings_in_exchange', to='collection.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
