# Generated by Django 2.0.3 on 2018-03-29 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180329_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.IntegerField(default=0, verbose_name='回复数'),
        ),
    ]
