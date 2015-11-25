# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('login_name', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('pwd', models.CharField(max_length=8)),
                ('surname', models.CharField(max_length=16)),
                ('given_name', models.CharField(max_length=64)),
                ('credit_card', models.CharField(max_length=16)),
                ('address', models.CharField(max_length=128)),
                ('phoneno', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, b'Score must be >= 0.'), django.core.validators.MaxValueValidator(10, b'Score must be <= 10.')])),
                ('txt', models.TextField(default=b'A')),
            ],
        ),
        migrations.CreateModel(
            name='Ord',
            fields=[
                ('oid', models.AutoField(serialize=False, primary_key=True)),
                ('timestmp', models.DateTimeField(null=True)),
                ('stat', models.CharField(max_length=16, null=True)),
                ('customer', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrdBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qty', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, b'Order quantity cannot be negative.')])),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, b'Rating must be >= 0.'), django.core.validators.MaxValueValidator(2, b'Rating must be <= 2.')])),
                ('opinion', models.ForeignKey(to='bookstore.Opinion')),
                ('rater', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.RemoveField(
            model_name='book',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='copies',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='book',
            name='frmt',
            field=models.CharField(max_length=1, null=True, choices=[(b'H', b'Hardcover'), (b'S', b'Softcover')]),
        ),
        migrations.AddField(
            model_name='book',
            name='keywords',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='sbj',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='yr',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0, b'Year cannot be less than 0!')]),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=14, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='ordbook',
            name='book',
            field=models.ForeignKey(to='bookstore.Book'),
        ),
        migrations.AddField(
            model_name='ordbook',
            name='oid',
            field=models.ForeignKey(to='bookstore.Ord'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='book',
            field=models.ForeignKey(to='bookstore.Book'),
        ),
        migrations.AddField(
            model_name='opinion',
            name='customer',
            field=models.ForeignKey(to='bookstore.Customer'),
        ),
        migrations.AlterUniqueTogether(
            name='rate',
            unique_together=set([('rater', 'opinion')]),
        ),
        migrations.AlterUniqueTogether(
            name='ordbook',
            unique_together=set([('oid', 'book')]),
        ),
        migrations.AlterUniqueTogether(
            name='opinion',
            unique_together=set([('customer', 'book')]),
        ),
    ]
