# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-06 07:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20200501_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
