# Generated by Django 4.1.3 on 2024-02-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creature',
            name='rarity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ccapi.rarity'),
        ),
    ]
