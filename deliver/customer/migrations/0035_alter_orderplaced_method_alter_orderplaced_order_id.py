# Generated by Django 5.0.6 on 2024-06-01 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0034_orderplaced_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='method',
            field=models.CharField(choices=[('Dine In', 'Dine In'), ('Pick Up', 'Pick Up')], max_length=10),
        ),
        migrations.AlterField(
            model_name='orderplaced',
            name='order_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
