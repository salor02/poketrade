# Generated by Django 5.0.6 on 2024-07-06 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0013_alter_feedback_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='published_at',
            field=models.DateTimeField(null=True),
        ),
    ]
