# Generated by Django 2.2.2 on 2019-07-28 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0010_trip_trip_tripstatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='trip_tripstatus',
            new_name='tripstatus',
        ),
    ]