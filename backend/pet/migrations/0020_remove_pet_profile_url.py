# Generated by Django 4.0.3 on 2023-07-25 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0019_pet_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='profile_url',
        ),
    ]
