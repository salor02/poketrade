# Generated by Django 5.0.6 on 2024-06-18 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_profile_paypal_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='img_url',
            new_name='profile_pic',
        ),
    ]
