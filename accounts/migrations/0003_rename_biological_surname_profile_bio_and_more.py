# Generated by Django 5.1.7 on 2025-03-25 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_biological_surname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='biological_surname',
            new_name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='current_surname',
        ),
        migrations.DeleteModel(
            name='Employment',
        ),
    ]
