# Generated by Django 3.1.7 on 2021-05-06 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0013_auto_20210506_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='note',
        ),
    ]