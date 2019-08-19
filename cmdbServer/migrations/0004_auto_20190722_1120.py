# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-07-22 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0003_monitors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servers',
            name='status',
        ),
        migrations.AddField(
            model_name='servers',
            name='use_status',
            field=models.SmallIntegerField(choices=[(0, '已启用'), (1, '未启用'), (2, '故障'), (3, '下线')], default=0, verbose_name='使用状态'),
        ),
    ]
