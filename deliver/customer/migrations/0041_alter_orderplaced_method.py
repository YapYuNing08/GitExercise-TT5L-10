# Generated by Django 5.0.6 on 2024-06-01 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0040_alter_orderplaced_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='method',
            field=models.CharField(choices=[('dine-in', 'dine-in'), ('pick-up', 'pick-up')], default='dine-in', max_length=10),
        ),
    ]