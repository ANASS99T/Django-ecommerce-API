# Generated by Django 5.0.4 on 2024-06-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_category_created_at_category_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
