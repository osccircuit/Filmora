# Generated by Django 5.1.7 on 2025-03-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('country', models.CharField(blank=True, max_length=200, verbose_name='Страна')),
                ('genre', models.CharField(blank=True, max_length=200, verbose_name='Жанр')),
            ],
        ),
    ]
