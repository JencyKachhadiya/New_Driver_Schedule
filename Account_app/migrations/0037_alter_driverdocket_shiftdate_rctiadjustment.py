# Generated by Django 4.2.1 on 2024-01-06 09:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0013_alter_clienttruckconnection_startdate_and_more'),
        ('Account_app', '0036_rctiexpense_clientname_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 6, 9, 27, 31, 627579, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.CreateModel(
            name='RctiAdjustment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truckNo', models.FloatField(default=0)),
                ('docketNumber', models.CharField(default='', max_length=10)),
                ('docketDate', models.DateField()),
                ('docketYard', models.CharField(default='', max_length=255)),
                ('noOfKm', models.FloatField(default=0)),
                ('invoiceQuantity', models.FloatField(default=0)),
                ('unit', models.CharField(default='', max_length=10)),
                ('unitPrice', models.FloatField(default=0)),
                ('totalExGST', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('Total', models.FloatField(default=0)),
                ('clientName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.client')),
                ('rctiReport', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Account_app.rctireport')),
            ],
        ),
    ]
