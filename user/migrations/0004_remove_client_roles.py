# Generated by Django 5.0.4 on 2024-05-18 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_client_first_name_alter_client_last_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='roles',
        ),
    ]