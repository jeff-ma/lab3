# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-08-17 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url_Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.CharField(max_length=50)),
                ('full_url', models.CharField(max_length=300)),
                ('http_status', models.IntegerField()),
                ('page_title', models.TextField()),
                ('wayback_url', models.CharField(default='none', max_length=300)),
                ('timestamp', models.CharField(default='none', max_length=50)),
            ],
        ),
    ]
