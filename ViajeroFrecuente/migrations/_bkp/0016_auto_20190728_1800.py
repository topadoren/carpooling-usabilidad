# Generated by Django 2.2.2 on 2019-07-28 21:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0015_auto_20190728_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qualification',
            name='givenby',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='givenby', to='ViajeroFrecuente.AppUser'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 28, 18, 0, 57, 286104)),
        ),
        migrations.AlterField(
            model_name='trip',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='ViajeroFrecuente.AppUser'),
        ),
        migrations.AlterUniqueTogether(
            name='qualification',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='qualification',
            name='user',
        ),
    ]
