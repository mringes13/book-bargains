# Generated by Django 3.1.7 on 2021-04-26 14:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0008_auto_20210426_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='uuid',
            field=models.CharField(blank=True, default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
