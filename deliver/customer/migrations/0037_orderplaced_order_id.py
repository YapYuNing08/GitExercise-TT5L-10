# Generated by Django 5.0.6 on 2024-06-01 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0036_remove_orderplaced_order_id_alter_orderplaced_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='order_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
