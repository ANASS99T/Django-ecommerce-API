# Generated by Django 5.0.4 on 2024-06-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled'), ('COMPLETE', 'Complete'), ('DELETED', 'Deleted')], default='PENDING', max_length=20),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
