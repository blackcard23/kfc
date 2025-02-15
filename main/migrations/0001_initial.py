# Generated by Django 4.2.14 on 2024-07-17 15:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', models.CharField(max_length=70, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Name')),
                ('slug', models.CharField(max_length=90, verbose_name='Slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('picture', models.ImageField(default='items/images.jpg', upload_to='items/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpg'])], verbose_name='Picture')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
    ]
