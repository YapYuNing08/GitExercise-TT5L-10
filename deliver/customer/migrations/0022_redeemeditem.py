# Generated by Django 5.0.6 on 2024-05-26 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0021_product_quantity_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedeemedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_redeemed', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.redemptionoption')),
            ],
        ),
    ]
