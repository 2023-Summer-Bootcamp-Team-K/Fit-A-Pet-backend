# Generated by Django 4.0.3 on 2023-07-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0020_remove_pet_profile_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='profile_url',
            field=models.URLField(blank=True, editable=False, null=True),
        ),
    ]
