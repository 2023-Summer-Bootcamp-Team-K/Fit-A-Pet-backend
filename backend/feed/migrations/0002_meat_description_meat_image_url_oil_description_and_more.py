# Generated by Django 4.2.3 on 2023-07-10 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meat',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='meat',
            name='image_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='oil',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='oil',
            name='image_url',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='supplement',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='supplement',
            name='image_url',
            field=models.URLField(null=True),
        ),
    ]
