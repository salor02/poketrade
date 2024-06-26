# Generated by Django 5.0.6 on 2024-06-18 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_card_owners_wishlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='collection.set'),
        ),
        migrations.AlterField(
            model_name='set',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='collection.game'),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to=settings.AUTH_USER_MODEL),
        ),
    ]
