# Generated by Django 5.0.6 on 2024-05-31 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0028_remove_customer_mobile_remove_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='redemptionoption',
            name='review',
            field=models.BooleanField(default=False),
        ),
    ]
