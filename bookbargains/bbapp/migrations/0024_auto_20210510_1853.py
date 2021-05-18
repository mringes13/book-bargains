# Generated by Django 3.1.7 on 2021-05-10 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0023_auto_20210509_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rating',
            name='numberofratings',
            field=models.FloatField(default=1.0),
        ),
    ]
