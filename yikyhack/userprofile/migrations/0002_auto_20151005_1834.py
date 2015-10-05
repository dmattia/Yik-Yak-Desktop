# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='latitude',
            field=models.FloatField(default=41.7055716),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='longitude',
            field=models.FloatField(default=-86.2353388),
            preserve_default=False,
        ),
    ]
