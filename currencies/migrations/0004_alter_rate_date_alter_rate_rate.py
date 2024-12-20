# Generated by Django 5.1.3 on 2024-12-03 14:53

import currencies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0003_alter_currency_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='date',
            field=models.DateField(validators=[currencies.models.date_not_in_the_future]),
        ),
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.FloatField(validators=[currencies.models.rate_greater_than_zero]),
        ),
    ]
