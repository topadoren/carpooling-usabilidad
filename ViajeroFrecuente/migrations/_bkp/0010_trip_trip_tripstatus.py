# Generated by Django 2.2.2 on 2019-07-28 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0009_auto_20190728_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='trip_tripstatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trip_status', to='ViajeroFrecuente.TripStatus'),
            preserve_default=False,
        ),
    ]
