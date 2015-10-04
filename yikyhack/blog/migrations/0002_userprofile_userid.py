# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='userID',
            field=models.CharField(default='842E2854-0147-472A-A146-EC1D5C9EB572', max_length=255),
            preserve_default=False,
        ),
    ]
