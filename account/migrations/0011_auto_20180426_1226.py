# Generated by Django 2.0.3 on 2018-04-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20180420_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.SmallIntegerField(choices=[(0, '注销'), (1, '正常')], default=0, verbose_name='账号状态'),
        ),
    ]
