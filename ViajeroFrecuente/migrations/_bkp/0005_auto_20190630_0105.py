# Generated by Django 2.2.2 on 2019-06-30 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0004_auto_20190629_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='trip_tripstatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='trip_status', to='ViajeroFrecuente.TripStatus'),
            preserve_default=False,
        ),
    ]