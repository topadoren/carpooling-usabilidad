# Generated by Django 2.2.2 on 2019-07-28 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0011_auto_20190728_1107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='tripstatus',
            new_name='status',
        ),
    ]
