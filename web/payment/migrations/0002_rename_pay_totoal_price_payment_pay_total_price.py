# Generated by Django 5.0.6 on 2024-06-24 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='pay_totoal_price',
            new_name='pay_total_price',
        ),
    ]
