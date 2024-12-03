# Generated by Django 5.1.3 on 2024-11-28 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_from', models.ForeignKey(db_column='currency_from', on_delete=django.db.models.deletion.CASCADE, related_name='currency_from', to='currencies.currency')),
                ('currency_to', models.ForeignKey(db_column='currency_to', on_delete=django.db.models.deletion.CASCADE, related_name='currency_to', to='currencies.currency')),
            ],
        ),
    ]
