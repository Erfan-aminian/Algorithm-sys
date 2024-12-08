# Generated by Django 4.2.16 on 2024-12-07 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_dynamicprocessmodel_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicprocessmodel',
            name='quantum',
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='dynamicprocessmodel',
            name='arrival_time',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='dynamicprocessmodel',
            name='burst_time',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='dynamicprocessmodel',
            name='priority',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dynamicprocessmodel',
            name='process_name',
            field=models.PositiveSmallIntegerField(),
        ),
    ]