# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_auto_20151125_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='desc',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='img',
            field=models.URLField(null=True),
        ),
    ]
