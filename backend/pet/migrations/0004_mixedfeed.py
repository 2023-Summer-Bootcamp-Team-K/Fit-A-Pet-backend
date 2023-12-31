# Generated by Django 4.2.3 on 2023-07-10 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_meat_oil_supplement'),
    ]

    operations = [
        migrations.CreateModel(
            name='MixedFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('meat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.meat')),
                ('oil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.oil')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.pet')),
                ('supplement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pet.supplement')),
            ],
        ),
    ]
