# Generated by Django 4.2.3 on 2023-07-06 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_data_code'),
        ('codeNumber', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='codenumber',
            name='device_num',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='data.data'),
        ),
    ]
