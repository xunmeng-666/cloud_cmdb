# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-14 09:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0013_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='command',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='指令'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdbServer.Job'),
        ),
    ]
