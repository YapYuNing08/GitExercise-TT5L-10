# Generated by Django 5.0.6 on 2024-06-08 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0049_cart_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='session_key',
        ),
    ]
