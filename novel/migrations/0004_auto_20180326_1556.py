# Generated by Django 2.0.3 on 2018-03-26 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0003_auto_20180326_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chaptername',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='name',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
