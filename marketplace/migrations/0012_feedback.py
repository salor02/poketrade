# Generated by Django 5.0.6 on 2024-06-26 08:29

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0011_alter_listing_options_alter_transaction_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(help_text='Valuta da 1 a 10', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='marketplace.transaction')),
                ('user_dst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_feedbacks', to=settings.AUTH_USER_MODEL)),
                ('user_src', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
