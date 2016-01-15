# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('time', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=30)),
                ('application', models.ForeignKey(to='authentication.Application', related_name='instances')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('email', models.CharField(primary_key=True, serialize=False, max_length=30)),
                ('name_surname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='instance',
            name='user',
            field=models.ForeignKey(to='authentication.User', related_name='instances'),
        ),
    ]
