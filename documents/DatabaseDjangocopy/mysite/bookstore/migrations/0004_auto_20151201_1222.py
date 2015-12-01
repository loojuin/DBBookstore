# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151024185721 on 2015-12-01 12:22
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0003_auto_20151125_1117'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ordbook',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ordbook',
            name='book',
        ),
        migrations.RemoveField(
            model_name='ordbook',
            name='oid',
        ),
        migrations.AddField(
            model_name='ord',
            name='qty',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, b'Order quantity cannot be negative.')]),
        ),
        migrations.DeleteModel(
            name='OrdBook',
        ),
    ]
