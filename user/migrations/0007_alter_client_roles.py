# Generated by Django 5.0.4 on 2024-05-22 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0005_remove_role_user'),
        ('user', '0006_alter_client_first_name_alter_client_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='roles',
            field=models.ManyToManyField(blank=True, to='roles.role'),
        ),
    ]
