# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-18 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlexpander3', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='url_address',
            name='image',
            field=models.CharField(default='none', max_length=300),
        ),
    ]
