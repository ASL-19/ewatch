# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-22 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='address',
            field=models.CharField(default=None, max_length=2048, verbose_name='Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='age',
            field=models.PositiveIntegerField(default=None, verbose_name='Age'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='participant',
            name='education',
            field=models.CharField(blank=True, choices=[('nodiploma', 'No Diploma'), ('highschool', 'High School Graduate'), ('bachelor', 'Bachelor Degree'), ('masters', 'Master Degree'), ('phd', 'PhD'), ('hozeh', 'Hozeh Graduated'), ('other', 'Other')], max_length=128, null=True, verbose_name='Education'),
        ),
        migrations.AddField(
            model_name='participant',
            name='ethnicity',
            field=models.CharField(blank=True, choices=[('persian', 'Persian'), ('azerbaijani', 'Azerbaijani - Turk'), ('kurd', 'Kurd'), ('lur', 'Lur'), ('arab', 'Arab'), ('baloch', 'Baloch'), ('turkmen', 'Turkmen'), ('other', 'Other'), ('noethnicity', "I don't believe in ethnical category")], max_length=128, null=True, verbose_name='Ethnicity'),
        ),
        migrations.AddField(
            model_name='participant',
            name='income',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Income Value'),
        ),
        migrations.AddField(
            model_name='participant',
            name='income_currency',
            field=models.CharField(blank=True, choices=[('toman', 'Toman'), ('dollar', 'Dollar'), ('euro', 'Euro'), ('other', 'Other')], max_length=64, null=True, verbose_name='Income Currency'),
        ),
        migrations.AddField(
            model_name='participant',
            name='married',
            field=models.CharField(blank=True, choices=[('married', 'Married'), ('single', 'Single (Never Married)'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], max_length=128, null=True, verbose_name='Married'),
        ),
        migrations.AddField(
            model_name='participant',
            name='religion',
            field=models.CharField(blank=True, choices=[('shia', "Muslim - Shi'a"), ('sunni', 'Muslim - Sunni'), ('christian', 'Christian'), ('jew', 'Jew'), ('zoroastrian', 'Zoroastrian'), ('bahai', "Baha'i"), ('sabian', 'Sabian'), ('ahlehaqq', 'Ahl-e Haqq'), ('other', 'Other'), ('noreligion', "I don't believe in religion")], max_length=128, null=True, verbose_name='Religious Affiliation'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='gender',
            field=models.CharField(choices=[('unset', 'Unset'), ('male', 'male'), ('female', 'female')], default=None, max_length=8, verbose_name='Gender'),
            preserve_default=False,
        ),
    ]
