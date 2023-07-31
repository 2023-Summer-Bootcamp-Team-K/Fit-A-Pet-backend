# Generated by Django 4.2.3 on 2023-07-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0004_mixedfeed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mixedfeed',
            name='meat',
        ),
        migrations.RemoveField(
            model_name='mixedfeed',
            name='oil',
        ),
        migrations.RemoveField(
            model_name='mixedfeed',
            name='pet',
        ),
        migrations.RemoveField(
            model_name='mixedfeed',
            name='supplement',
        ),
        # migrations.AddField(
        #     model_name='pet',
        #     name='feed',
        #     field=models.CharField(blank=True, max_length=32),
        # ),
        # migrations.AddField(
        #     model_name='pet',
        #     name='sore_spot',
        #     field=models.CharField(blank=True, max_length=10),
        # ),
        migrations.DeleteModel(
            name='Meat',
        ),
        migrations.DeleteModel(
            name='MixedFeed',
        ),
        migrations.DeleteModel(
            name='Oil',
        ),
        migrations.DeleteModel(
            name='Supplement',
        ),
    ]
