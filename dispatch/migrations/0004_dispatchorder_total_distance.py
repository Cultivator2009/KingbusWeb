# Generated by Django 4.0.1 on 2022-03-18 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatch', '0003_dispatchestimate_pricebycar'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatchorder',
            name='total_distance',
            field=models.CharField(default='999', max_length=4),
            preserve_default=False,
        ),
    ]