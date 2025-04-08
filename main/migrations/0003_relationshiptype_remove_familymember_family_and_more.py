# Generated by Django 5.2 on 2025-04-08 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_family_user_alter_relationship_from_member_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('bidirectional', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='familymember',
            name='family',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='to_member',
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='from_member',
        ),
        migrations.CreateModel(
            name='FamilyTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('family_tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='main.familytree')),
            ],
        ),
        migrations.CreateModel(
            name='PersonRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_tree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='main.familytree')),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_relationships', to='main.person')),
                ('to_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_relationships', to='main.person')),
                ('relationship_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.relationshiptype')),
            ],
            options={
                'unique_together': {('from_person', 'to_person', 'relationship_type')},
            },
        ),
        migrations.DeleteModel(
            name='Family',
        ),
        migrations.DeleteModel(
            name='FamilyMember',
        ),
        migrations.DeleteModel(
            name='Relationship',
        ),
    ]
