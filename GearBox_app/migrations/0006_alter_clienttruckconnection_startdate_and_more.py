# Generated by Django 4.2.2 on 2024-02-04 12:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0005_alter_clienttruckconnection_startdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 402955, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 402346, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 402346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 402955, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 402955, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 401350, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 1, 12, 46, 45, 402346, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 4, 12, 46, 45, 402346, tzinfo=datetime.timezone.utc)),
        ),
    ]
