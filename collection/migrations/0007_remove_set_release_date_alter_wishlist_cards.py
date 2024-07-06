# Generated by Django 5.0.6 on 2024-07-05 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_card_description_card_move1_card_move2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='set',
            name='release_date',
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='cards',
            field=models.ManyToManyField(related_name='wishlists', to='collection.card'),
        ),
    ]