# Generated by Django 2.0.6 on 2018-06-29 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20180629_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesshowing',
            name='time_showing',
            field=models.DateTimeField(null=True),
        ),
    ]
