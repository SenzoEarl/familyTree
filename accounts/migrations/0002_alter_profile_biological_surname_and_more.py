# Generated by Django 5.1.7 on 2025-03-25 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='biological_surname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='current_surname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
