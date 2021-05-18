# Generated by Django 3.1.7 on 2021-05-12 05:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0027_auto_20210512_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='message',
        ),
        migrations.AddField(
            model_name='message',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction', to='bbapp.transaction'),
        ),
    ]
