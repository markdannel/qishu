# Generated by Django 2.0.3 on 2018-04-11 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0005_auto_20180411_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='name',
            name='yearrank',
        ),
        migrations.AddField(
            model_name='name',
            name='weekrank',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='周榜'),
        ),
        migrations.AlterField(
            model_name='name',
            name='monthrank',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='月榜'),
        ),
    ]
