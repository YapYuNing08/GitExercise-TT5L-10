# Generated by Django 5.0.6 on 2024-06-01 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0037_orderplaced_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='order_id',
        ),
    ]
