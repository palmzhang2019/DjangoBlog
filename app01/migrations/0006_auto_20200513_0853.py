# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-13 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20200506_0722'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='nike_name',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='nike_name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
