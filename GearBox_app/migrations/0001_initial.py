# Generated by Django 4.2.2 on 2023-11-07 11:36

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminTruck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminTruckNumber', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('clientId', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('docketGiven', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driverId', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='Phone number must be a 10-digit number without any special characters or spaces.', regex='^\\d{10}$')])),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NatureOfLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RateCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_card_name', models.CharField(max_length=255, unique=True)),
                ('tds', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Surcharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surcharge_Name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ThresholdNightShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_amount_per_night_shift', models.FloatField(default=0)),
                ('loading_cost_per_cubic_meter_included', models.BooleanField(default=False)),
                ('km_cost_included', models.BooleanField(default=False)),
                ('surcharge_included', models.BooleanField(default=False)),
                ('transfer_cost_included', models.BooleanField(default=False)),
                ('return_cost_included', models.BooleanField(default=False)),
                ('standby_cost_included', models.BooleanField(default=False)),
                ('waiting_cost_included', models.BooleanField(default=False)),
                ('call_out_fees_included', models.BooleanField(default=False)),
                ('min_load_in_cubic_meters', models.FloatField(default=0)),
                ('min_load_in_cubic_meters_return_to_yard', models.FloatField(default=0)),
                ('return_to_yard_grace', models.FloatField(default=0)),
                ('return_to_tipping_grace', models.FloatField(default=0)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 653582, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
            ],
        ),
        migrations.CreateModel(
            name='ThresholdDayShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold_amount_per_day_shift', models.FloatField(default=0)),
                ('loading_cost_per_cubic_meter_included', models.BooleanField(default=False)),
                ('km_cost_included', models.BooleanField(default=False)),
                ('surcharge_included', models.BooleanField(default=False)),
                ('transfer_cost_included', models.BooleanField(default=False)),
                ('return_cost_included', models.BooleanField(default=False)),
                ('standby_cost_included', models.BooleanField(default=False)),
                ('waiting_cost_included', models.BooleanField(default=False)),
                ('call_out_fees_included', models.BooleanField(default=False)),
                ('min_load_in_cubic_meters', models.FloatField(default=0)),
                ('min_load_in_cubic_meters_return_to_yard', models.FloatField(default=0)),
                ('return_to_yard_grace', models.FloatField(default=0)),
                ('return_to_tipping_grace', models.FloatField(default=0)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 653156, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
            ],
        ),
        migrations.CreateModel(
            name='OnLease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hourly_subscription_charge', models.FloatField(default=0)),
                ('daily_subscription_charge', models.FloatField(default=0)),
                ('weekly_subscription_charge', models.FloatField(default=0)),
                ('over_time_charge', models.FloatField(default=0)),
                ('surcharge_included', models.BooleanField(default=True)),
                ('transfer_cost_applicable', models.BooleanField(default=True)),
                ('return_cost_applicable', models.BooleanField(default=True)),
                ('standby_cost_per_slot_applicable', models.BooleanField(default=True)),
                ('waiting_cost_per_minute_applicable', models.BooleanField(default=True)),
                ('call_out_fees_applicable', models.BooleanField(default=True)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 653582, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=None, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.driver')),
                ('reason', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.natureofleave')),
            ],
        ),
        migrations.CreateModel(
            name='Grace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('load_km_grace', models.FloatField(default=0)),
                ('transfer_km_grace', models.FloatField(default=0)),
                ('return_km_grace', models.FloatField(default=0)),
                ('standby_time_grace_in_minutes', models.FloatField(default=0)),
                ('chargeable_standby_time_starts_after', models.FloatField(default=0)),
                ('waiting_time_grace_in_minutes', models.FloatField(default=0)),
                ('chargeable_waiting_time_starts_after', models.FloatField(default=0)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 653582, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
            ],
        ),
        migrations.CreateModel(
            name='CostParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loading_cost_per_cubic_meter', models.FloatField(default=0)),
                ('km_cost', models.FloatField(default=0)),
                ('surcharge_cost', models.FloatField(default=0)),
                ('transfer_cost', models.FloatField(default=0)),
                ('return_load_cost', models.FloatField(default=0)),
                ('return_km_cost', models.FloatField(default=0)),
                ('standby_time_slot_size', models.PositiveIntegerField(default=0)),
                ('standby_cost_per_slot', models.FloatField(default=0)),
                ('waiting_cost_per_minute', models.FloatField(default=0)),
                ('call_out_fees', models.FloatField(default=0)),
                ('demurrage_fees', models.FloatField(default=0)),
                ('cancellation_fees', models.FloatField(default=0)),
                ('clientPayableGst', models.FloatField(default=10.0)),
                ('start_date', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 652144, tzinfo=datetime.timezone.utc))),
                ('end_date', models.DateField(blank=True, null=True)),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
                ('surcharge_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.surcharge')),
            ],
        ),
        migrations.CreateModel(
            name='ClientTruckConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('truckType', models.CharField(choices=[('Embedded', 'Embedded'), ('Casual', 'Casual')], default='Embedded', max_length=254)),
                ('clientTruckId', models.PositiveIntegerField(default=0)),
                ('startDate', models.DateField(default=datetime.datetime(2023, 11, 7, 11, 36, 30, 654582, tzinfo=datetime.timezone.utc))),
                ('endDate', models.DateField(blank=True, null=True)),
                ('clientId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.client')),
                ('rate_card_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.ratecard')),
                ('truckNumber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.admintruck')),
            ],
        ),
    ]
