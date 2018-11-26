# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-24 17:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0005_auto_20181124_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to=settings.AUTH_USER_MODEL),
        ),
    ]
