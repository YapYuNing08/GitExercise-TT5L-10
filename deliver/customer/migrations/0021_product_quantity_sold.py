# Generated by Django 5.0.6 on 2024-05-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_sold',
            field=models.IntegerField(default=0),
        ),
    ]