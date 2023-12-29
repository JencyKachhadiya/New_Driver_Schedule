# Generated by Django 4.2.1 on 2023-12-10 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0006_alter_driverdocket_shiftdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 10, 9, 8, 50, 8036, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='atPlant',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='beginUnload',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='endPour',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='load',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='loadComplete',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='onJob',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='status',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='toJob',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='toPlant',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='wash',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]