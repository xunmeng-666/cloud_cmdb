# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-14 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0014_auto_20190814_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='script',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='cmdbServer.Job'),
        ),
    ]
