# Generated by Django 5.0.6 on 2024-06-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_images/default/profile_picture.png', null=True, upload_to='profile_images/%Y/%m/%d/', verbose_name='프로필 사진'),
        ),
    ]
