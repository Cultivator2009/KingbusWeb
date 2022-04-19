# Generated by Django 4.0.1 on 2022-04-06 08:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0009_rename_reservation_confirmed_dispatch_dispatch_status'),
        ('user', '0002_remove_companyacc_id_remove_driveracc_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KingbusReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('star', models.CharField(max_length=3)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('dispatch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dispatch.dispatch')),
                ('driverorcompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_driverorcpmpany', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]