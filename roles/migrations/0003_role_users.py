# Generated by Django 5.0.4 on 2024-05-18 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0002_permission_alter_role_permissions'),
        ('user', '0004_remove_client_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(related_name='roles', to='user.client'),
        ),
    ]
