# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-06 10:19
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0006_auto_20190726_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Users', models.FileField(upload_to='', verbose_name=django.contrib.auth.models.User)),
                ('tasks', django.contrib.postgres.fields.jsonb.JSONField()),
                ('result', models.CharField(blank=True, max_length=16, null=True, verbose_name='执行结果')),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '任务',
                'verbose_name_plural': '任务',
            },
        ),
    ]
