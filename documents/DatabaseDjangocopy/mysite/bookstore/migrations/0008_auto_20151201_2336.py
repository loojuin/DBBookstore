# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_auto_20151201_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0, b'Order quantity cannot be negative.')])),
                ('book', models.ForeignKey(to='bookstore.Book')),
                ('customer', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set([('customer', 'book')]),
        ),
    ]
