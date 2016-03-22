# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='char_icons'),
        ),
        migrations.AlterField(
            model_name='player',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='player_icons'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='date_ended',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Player'),
        ),
    ]