# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20151024185721 on 2015-12-05 03:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0017_auto_20151205_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ord',
            name='customer',
        ),
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
        migrations.DeleteModel(
            name='Ord',
        ),
        migrations.DeleteModel(
            name='OrdBook',
        ),
    ]
