# Generated by Django 4.2.16 on 2024-11-22 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_dynamicprocessmodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicprocessmodel',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]