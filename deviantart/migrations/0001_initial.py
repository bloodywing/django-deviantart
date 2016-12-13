# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-10 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.IntegerField(default=0)),
                ('access_token', models.CharField(default=None, max_length=50)),
                ('refresh_token', models.CharField(default=None, max_length=40)),
                ('expires_at', models.DateTimeField(default=None)),
            ],
        ),
    ]
