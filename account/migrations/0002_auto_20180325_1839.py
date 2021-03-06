# Generated by Django 2.0.3 on 2018-03-25 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=128, verbose_name='用户名称* （带*为必填项）'),
        ),
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=128, verbose_name='密码*'),
        ),
        migrations.AlterField(
            model_name='account',
            name='personalized_signature',
            field=models.CharField(blank=True, help_text='我最帅', max_length=128, null=True, verbose_name='个性签名'),
        ),
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(max_length=128, unique=True, verbose_name='手机号*'),
        ),
    ]
