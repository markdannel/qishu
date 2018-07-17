# Generated by Django 2.0.3 on 2018-03-26 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0002_auto_20180323_2132'),
        ('account', '0002_auto_20180325_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookshelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.IntegerField(blank=True, default=1)),
                ('bookname', models.CharField(blank=True, max_length=128, null=True, verbose_name='书名')),
                ('username', models.CharField(blank=True, max_length=128, null=True, verbose_name='用户名')),
                ('chaptername', models.CharField(blank=True, max_length=128, null=True, verbose_name='章节名')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.Name')),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='最近登录日期'),
        ),
        migrations.AlterField(
            model_name='account',
            name='personalized_signature',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='个性签名'),
        ),
        migrations.AlterField(
            model_name='account',
            name='picture',
            field=models.ImageField(blank=True, default='Imag/default_img.jpg', null=True, upload_to='Imag/%Y/%m/%d', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='bookshelf',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account'),
        ),
    ]
