# Generated by Django 4.2.3 on 2023-07-10 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='gender',
            field=models.CharField(choices=[('unspayed female', 'Unspayed Female'), ('spayed female', 'Spayed Female'), ('unneutered male', 'Unneutered Male'), ('neutered male', 'Neutered Male')], default='unspated female', max_length=20),
        ),
        migrations.AddField(
            model_name='pet',
            name='profile_url',
            field=models.ImageField(blank=True, upload_to='fitapet/'),
        ),
    ]
