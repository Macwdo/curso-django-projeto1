# Generated by Django 4.0.5 on 2022-06-30 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='preparation',
            new_name='preparation_time',
        ),
    ]
