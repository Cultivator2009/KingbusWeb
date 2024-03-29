# Generated by Django 4.0.1 on 2022-03-02 02:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DispatchOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('way', models.CharField(max_length=2)),
                ('purpose', models.CharField(max_length=100)),
                ('reference', models.TextField(blank=True)),
                ('departure', models.CharField(max_length=255)),
                ('arrival', models.CharField(max_length=255)),
                ('stopover', models.TextField(blank=True)),
                ('departure_date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_date', models.DateField(blank=True, null=True)),
                ('arrival_time', models.TimeField(blank=True, null=True)),
                ('is_driver', models.BooleanField(default=False)),
                ('total_number', models.CharField(max_length=10)),
                ('convenience', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'kingbus_dispatch_order',
            },
        ),
        migrations.CreateModel(
            name='RegularlyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.CharField(max_length=1)),
                ('term_begin', models.DateField()),
                ('term_end', models.DateField()),
            ],
            options={
                'db_table': 'kingbus_regulary_order',
            },
        ),
        migrations.CreateModel(
            name='DispatchEstimate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(max_length=10)),
                ('bus_cnt', models.CharField(max_length=5)),
                ('bus_type', models.CharField(max_length=64)),
                ('is_tollgate', models.BooleanField(default=False)),
                ('is_parking', models.BooleanField(default=False)),
                ('is_accomodation', models.BooleanField(default=False)),
                ('is_meal', models.BooleanField(default=False)),
                ('is_convenience', models.BooleanField(default=False)),
                ('driverorcompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchorder')),
            ],
            options={
                'db_table': 'kingbus_estimate',
            },
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='dispatch.dispatchorder')),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('estimate_order_time', models.DateTimeField(blank=True, null=True)),
                ('estimate_confirmed_time', models.DateTimeField(blank=True, null=True)),
                ('reservation_confirmed', models.BooleanField(default=False)),
                ('regularly', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.regularlyorder')),
                ('selected_estimate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatchestimate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'kingbus_dispatch',
            },
        ),
    ]
