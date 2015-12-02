# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_auto_20151201_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
