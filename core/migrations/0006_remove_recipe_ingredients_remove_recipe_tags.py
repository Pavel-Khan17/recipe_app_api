# Generated by Django 5.0.1 on 2024-02-15 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_recipe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
    ]
