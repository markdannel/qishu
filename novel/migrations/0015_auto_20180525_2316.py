# Generated by Django 2.0.3 on 2018-05-25 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0014_auto_20180517_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='name_id',
            field=models.CharField(max_length=255, unique=True, verbose_name='书编号'),
        ),
    ]