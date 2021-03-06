# Generated by Django 2.0.3 on 2018-04-20 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0006_auto_20180411_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='Websetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='名称')),
                ('key', models.CharField(max_length=128, unique=True, verbose_name='key')),
                ('value', models.CharField(max_length=128, verbose_name='路径')),
                ('time', models.DateTimeField(auto_now=True, null=True, verbose_name='上次修改时间')),
            ],
            options={
                'verbose_name': '网站设置',
                'verbose_name_plural': '网站设置',
            },
        ),
        migrations.AlterModelOptions(
            name='chaptername',
            options={'ordering': ['num_id'], 'verbose_name': '小说章节', 'verbose_name_plural': '小说章节'},
        ),
        migrations.AlterModelOptions(
            name='name',
            options={'verbose_name': '小说', 'verbose_name_plural': '小说'},
        ),
        migrations.AlterField(
            model_name='chaptername',
            name='id_name',
            field=models.CharField(max_length=15, verbose_name='书编号'),
        ),
        migrations.AlterField(
            model_name='chaptername',
            name='num_id',
            field=models.CharField(max_length=15, verbose_name='章节号'),
        ),
        migrations.AlterField(
            model_name='chaptername',
            name='url',
            field=models.CharField(max_length=255, verbose_name='获取URL'),
        ),
        migrations.AlterField(
            model_name='chaptername',
            name='xs_chaptername',
            field=models.CharField(max_length=255, verbose_name='章节名'),
        ),
        migrations.AlterField(
            model_name='chaptername',
            name='xs_content',
            field=models.TextField(verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='name',
            name='category',
            field=models.CharField(max_length=255, verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='name',
            name='name_id',
            field=models.CharField(max_length=255, verbose_name='书编号'),
        ),
        migrations.AlterField(
            model_name='name',
            name='xs_author',
            field=models.CharField(max_length=255, verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='name',
            name='xs_name',
            field=models.CharField(max_length=255, verbose_name='小说名'),
        ),
    ]
