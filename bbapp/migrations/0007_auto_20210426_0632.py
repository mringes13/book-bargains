# Generated by Django 3.1.7 on 2021-04-26 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbapp', '0006_cart_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='items',
            new_name='cartitem',
        ),
    ]