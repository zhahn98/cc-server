# Generated by Django 4.1.3 on 2024-03-21 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccapi', '0003_alter_creaturecategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='No bio provided', max_length=500),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='User', max_length=20),
        ),
    ]