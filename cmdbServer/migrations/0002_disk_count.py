# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-24 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='disk',
            name='count',
            field=models.IntegerField(blank=True, null=True, verbose_name='磁盘数量'),
        ),
    ]
