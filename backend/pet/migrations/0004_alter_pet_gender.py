# Generated by Django 4.0.3 on 2023-07-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_pet_feed_pet_sore_spot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='gender',
            field=models.CharField(choices=[('unspayed female', 'Unspayed Female'), ('spayed female', 'Spayed Female'), ('unneutered male', 'Unneutered Male'), ('neutered male', 'Neutered Male')], default='unspayed female', max_length=20),
        ),
    ]
