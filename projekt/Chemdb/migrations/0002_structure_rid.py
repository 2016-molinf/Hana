# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-08 14:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chemdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='rId',
            field=models.TextField(default='MI-H-'),
        ),
    ]
