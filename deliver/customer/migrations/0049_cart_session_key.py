# Generated by Django 5.0.6 on 2024-06-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0048_merge_20240607_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='session_key',
            field=models.CharField(default='4e7dc69870904df996d3f8ec22a466d1', max_length=40),
        ),
    ]