# Generated by Django 4.2.3 on 2023-07-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_meat_description_meat_image_url_oil_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meat',
            name='image_url',
            field=models.URLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='oil',
            name='image_url',
            field=models.URLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='supplement',
            name='image_url',
            field=models.URLField(max_length=500, null=True),
        ),
    ]
