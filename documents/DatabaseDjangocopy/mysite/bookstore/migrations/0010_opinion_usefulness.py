# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0009_cart_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='opinion',
            name='usefulness',
            field=models.IntegerField(default=0),
        ),
    ]
