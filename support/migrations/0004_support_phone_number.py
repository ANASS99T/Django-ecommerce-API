# Generated by Django 5.0.4 on 2024-06-02 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_support_deleted_at_support_parent_support_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
