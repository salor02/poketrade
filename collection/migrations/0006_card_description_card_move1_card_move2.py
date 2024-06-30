# Generated by Django 5.0.6 on 2024-06-30 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_alter_wishlist_cards'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='description',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='move1',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='move2',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]