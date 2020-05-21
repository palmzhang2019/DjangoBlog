# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-05-01 09:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20200501_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlDetail',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Article')),
            ],
            options={
                'verbose_name': 'ArticleDetail',
                'verbose_name_plural': 'ArticleDetails',
            },
        ),
    ]