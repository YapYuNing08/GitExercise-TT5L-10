# Generated by Django 5.0.4 on 2024-05-09 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
