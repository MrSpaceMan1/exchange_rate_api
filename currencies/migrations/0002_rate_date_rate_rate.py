# Generated by Django 5.1.3 on 2024-11-29 15:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 11, 29, 16, 14, 41, 307512)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='rate',
            field=models.FloatField(default=1984),
            preserve_default=False,
        ),
    ]
