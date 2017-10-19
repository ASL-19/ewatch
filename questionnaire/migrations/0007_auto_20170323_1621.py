# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-23 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_auto_20170323_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='questionnaire.ChoiceSet', verbose_name='Choice Set'),
        ),
        migrations.AlterField(
            model_name='choice',
            name='order',
            field=models.PositiveIntegerField(verbose_name='Order'),
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together=set([('order', 'choice_set')]),
        ),
    ]
