# Generated by Django 2.2.2 on 2019-07-28 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ViajeroFrecuente', '0012_auto_20190728_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='user',
            field=models.IntegerField(),
        ),
    ]