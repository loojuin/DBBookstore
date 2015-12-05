# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151024185721 on 2015-12-04 17:18
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0015_auto_20151204_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ord',
            fields=[
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('timestmp', models.DateTimeField(null=True)),
                ('stat', models.CharField(max_length=16, null=True)),
                ('qty', models.CommaSeparatedIntegerField(default=0, max_length=128, validators=[django.core.validators.MinValueValidator(0, b'Order quantity cannot be negative.')])),
                ('book', models.ManyToManyField(to='bookstore.Book')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookstore.Customer')),
            ],
        ),
    ]
