# Generated by Django 5.0.6 on 2024-06-03 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0043_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='redeemeditem',
            name='last_redeemed_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
