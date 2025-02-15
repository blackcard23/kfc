# Generated by Django 5.0.7 on 2024-07-24 11:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_category_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderelement',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='main.order'),
        ),
    ]
