<<<<<<< HEAD
# Generated by Django 4.2.2 on 2023-10-23 05:09
=======
# Generated by Django 4.2.1 on 2023-10-23 05:52
>>>>>>> 57a541857efce0fa54b4cec3a7a40f1651793c6a

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('GearBox_app', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasePlant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basePlant', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PastTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(default=None, null=True)),
                ('Truck_No', models.CharField(default=None, max_length=255, null=True)),
                ('Truck_Type', models.CharField(default=None, max_length=255, null=True)),
                ('Replacement', models.CharField(default=None, max_length=255, null=True)),
                ('Driver_Name', models.CharField(default=None, max_length=255, null=True)),
                ('Docket_NO', models.CharField(default=None, max_length=255, null=True)),
                ('Load_Time', models.TimeField(default=None, null=True)),
                ('Return_time', models.TimeField(default=None, null=True)),
                ('Load_qty', models.PositiveIntegerField(default=None, null=True)),
                ('Doc_KMs', models.FloatField(default=None, null=True)),
                ('Actual_KMs', models.FloatField(default=None, null=True)),
                ('waiting_time_starts_Onsite', models.PositiveIntegerField(default=None, null=True)),
                ('waiting_time_end_offsite', models.PositiveIntegerField(default=None, null=True)),
                ('Total_minutes', models.IntegerField(default=None, null=True)),
                ('Returned_Qty', models.PositiveIntegerField(default=None, null=True)),
                ('Returned_KM', models.FloatField(default=None, null=True)),
                ('Returned_to_Yard', models.BooleanField(default=None, null=True)),
                ('Comment', models.TextField(default=None, null=True)),
                ('Transfer_KM', models.FloatField(default=None, null=True)),
                ('stand_by_Start_Time', models.PositiveIntegerField(default=None, null=True)),
                ('stand_by_end_time', models.PositiveIntegerField(default=None, null=True)),
                ('stand_by_total_minute', models.IntegerField(default=None, null=True)),
                ('Stand_by_slot', models.CharField(default=None, max_length=255, null=True)),
                ('category', models.CharField(default=None, max_length=255, null=True)),
                ('call_out', models.CharField(default=None, max_length=255, null=True)),
                ('standby_minute', models.IntegerField(default=None, null=True)),
                ('ShiftType', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], default=None, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('stateName', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RCTI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truckNo', models.FloatField(default=0)),
                ('docketNumber', models.CharField(default='', max_length=10)),
                ('docketDate', models.DateField()),
                ('docketYard', models.CharField(default='', max_length=255)),
                ('noOfKm', models.FloatField(default=0)),
                ('cubicMl', models.FloatField(default=0)),
                ('cubicMiAndKmsCost', models.FloatField(default=0)),
                ('destination', models.CharField(default='Not given', max_length=255)),
                ('cartageGSTPayable', models.FloatField(default=0)),
                ('cartageTotalExGST', models.FloatField(default=0)),
                ('cartageTotal', models.FloatField(default=0)),
                ('transferKM', models.FloatField(default=0)),
                ('transferKMCost', models.FloatField(default=0)),
                ('transferKMGSTPayable', models.FloatField(default=0)),
                ('transferKMTotalExGST', models.FloatField(default=0)),
                ('transferKMTotal', models.FloatField(default=0)),
                ('returnKm', models.FloatField(default=0)),
                ('returnPerKmPerCubicMeterCost', models.FloatField(default=0)),
                ('returnKmGSTPayable', models.FloatField(default=0)),
                ('returnKmTotalExGST', models.FloatField(default=0)),
                ('returnKmTotal', models.FloatField(default=0)),
                ('waitingTimeSCHED', models.FloatField(default=0)),
                ('waitingTimeSCHEDCost', models.FloatField(default=0)),
                ('waitingTimeSCHEDGSTPayable', models.FloatField(default=0)),
                ('waitingTimeSCHEDTotalExGST', models.FloatField(default=0)),
                ('waitingTimeSCHEDTotal', models.FloatField(default=0)),
                ('waitingTimeInMinutes', models.FloatField(default=0, max_length=255)),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('waitingTimeGSTPayable', models.FloatField(default=0)),
                ('waitingTimeTotalExGST', models.FloatField(default=0)),
                ('waitingTimeTotal', models.FloatField(default=0)),
                ('standByPerHalfHourCost', models.FloatField(default=0)),
                ('standByPerHalfHourDuration', models.FloatField(default=0)),
                ('standByUnit', models.CharField(choices=[('minute', 'MINUTE'), ('slot', 'SLOT')], default='minute', max_length=6)),
                ('standByGSTPayable', models.FloatField(default=0)),
                ('standByTotalExGST', models.FloatField(default=0)),
                ('standByTotal', models.FloatField(default=0)),
                ('minimumLoad', models.FloatField(default=0)),
                ('loadCost', models.FloatField(default=0)),
                ('minimumLoadGSTPayable', models.FloatField(default=0)),
                ('minimumLoadTotalExGST', models.FloatField(default=0)),
                ('minimumLoadTotal', models.FloatField(default=0)),
                ('surcharge_fixed_normal', models.FloatField(default=0)),
                ('surcharge_fixed_sunday', models.FloatField(default=0)),
                ('surcharge_fixed_public_holiday', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_normal', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_sunday', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_public_holiday', models.FloatField(default=0)),
                ('surcharge_duration', models.FloatField(default=0)),
                ('surchargeUnit', models.CharField(choices=[('minute', 'MINUTE'), ('slot', 'SLOT')], default='minute', max_length=6)),
                ('surchargeGSTPayable', models.FloatField(default=0)),
                ('surchargeTotalExGST', models.FloatField(default=0)),
                ('surchargeTotal', models.FloatField(default=0)),
                ('others', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('othersCost', models.FloatField(default=0)),
                ('othersGSTPayable', models.FloatField(default=0)),
                ('othersTotalExGST', models.FloatField(default=0)),
                ('othersTotal', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='RCTIDocketAdjustment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noOfKm', models.FloatField(default=0)),
                ('noOfKmCost', models.FloatField(default=0)),
                ('transferKM', models.PositiveIntegerField(default=0)),
                ('transferKMCost', models.FloatField(default=0)),
                ('returnKm', models.FloatField(default=0)),
                ('returnPerKmPerCubicMeterCost', models.FloatField(default=0)),
                ('waitingTimeInMinutes', models.CharField(max_length=255)),
                ('waitingTimeCost', models.FloatField(default=0)),
                ('minimumLoad', models.FloatField(default=0)),
                ('surcharge_fixed_normal', models.FloatField(default=0)),
                ('surcharge_fixed_sunday', models.FloatField(default=0)),
                ('surcharge_fixed_public_holiday', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_normal', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_sunday', models.FloatField(default=0)),
                ('surcharge_per_cubic_meters_public_holiday', models.FloatField(default=0)),
                ('surcharge_duration', models.FloatField(default=0)),
                ('cubicMl', models.PositiveIntegerField(default=0)),
                ('cubicMlCost', models.FloatField(default=0)),
                ('minLoad', models.PositiveIntegerField(default=0)),
                ('loadCost', models.FloatField(default=0)),
                ('standByPerHalfHourCost', models.FloatField(default=0)),
                ('standByPerHalfHourDuration', models.FloatField(default=0)),
                ('others', models.PositiveIntegerField(default=0)),
                ('othersCost', models.FloatField(default=0)),
                ('GSTPayable', models.FloatField(default=0)),
                ('TotalExGST', models.FloatField(default=0)),
                ('Total', models.FloatField(default=0)),
                ('DocketNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account_app.rcti')),
            ],
        ),
        migrations.CreateModel(
            name='DriverTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(default=False)),
                ('shiftType', models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], max_length=200)),
                ('numberOfLoads', models.FloatField(default=0)),
                ('truckNo', models.IntegerField()),
                ('shiftDate', models.DateField(default=None, null=True)),
                ('startTime', models.CharField(max_length=200)),
                ('endTime', models.CharField(max_length=200)),
                ('loadSheet', models.FileField(upload_to='static/img/finalloadSheet')),
                ('comment', models.CharField(default='None', max_length=200)),
                ('clientName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.client')),
                ('driverId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.driver')),
            ],
        ),
        migrations.CreateModel(
            name='DriverDocket',
            fields=[
                ('docketId', models.AutoField(primary_key=True, serialize=False)),
                ('shiftDate', models.DateField(default=datetime.datetime(2023, 10, 23, 5, 9, 41, 841895, tzinfo=datetime.timezone.utc), null=True)),
                ('docketNumber', models.IntegerField()),
                ('docketFile', models.FileField(upload_to='static/img/docketFiles')),
                ('noOfKm', models.FloatField(default=0)),
                ('transferKM', models.FloatField(default=0)),
                ('returnToYard', models.BooleanField(default=False)),
                ('returnQty', models.FloatField(default=0)),
                ('returnKm', models.FloatField(default=0)),
                ('waitingTimeStart', models.CharField(max_length=200)),
                ('waitingTimeEnd', models.CharField(max_length=200)),
                ('totalWaitingInMinute', models.FloatField(default=0)),
                ('surcharge_type', models.CharField(choices=[('fixed normal', 'FIXED NORMAL'), ('fixed sunday', 'FIXED SUNDAY'), ('fixed public holiday', 'FIXED PUBLIC HOLIDAY'), ('per cubic meters normal', 'PER CUBIC METERS NORMAL'), ('per cubic meters sunday', 'PER CUBIC METERS SUNDAY'), ('per cubic meters public holiday', 'PER CUBIC METERS PUBLIC HOLIDAY')], default='fixed normal', max_length=31)),
                ('surcharge_duration', models.FloatField(default=0)),
                ('cubicMl', models.FloatField(default=0)),
                ('standByStartTime', models.CharField(max_length=200)),
                ('standByEndTime', models.CharField(max_length=200)),
                ('others', models.FloatField(default=0)),
                ('comment', models.CharField(default='None', max_length=255, null=True)),
                ('basePlant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account_app.baseplant')),
                ('tripId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Account_app.drivertrip')),
            ],
            options={
                'unique_together': {('docketNumber', 'shiftDate')},
            },
        ),
    ]
