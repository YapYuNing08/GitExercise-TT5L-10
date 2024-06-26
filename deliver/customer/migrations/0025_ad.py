# Generated by Django 5.0.4 on 2024-05-30 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0024_remove_redeemeditem_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='ads/')),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
