# Generated by Django 5.0.6 on 2024-06-18 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_delete_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='paypal_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
