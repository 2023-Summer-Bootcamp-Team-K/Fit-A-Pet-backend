# Generated by Django 4.2.3 on 2023-07-18 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codeNumber', '0006_alter_codenumber_device_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codenumber',
            name='device_num',
            field=models.CharField(max_length=50),
        ),
    ]
