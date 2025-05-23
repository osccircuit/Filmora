# Generated by Django 5.1.7 on 2025-04-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_usermovie_mark'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date_to_pay',
            field=models.DateField(blank=True, null=True, verbose_name='Дата оплаты'),
        ),
        migrations.AddField(
            model_name='user',
            name='type_of_sub',
            field=models.CharField(choices=[('FR', 'FREE'), ('ST', 'STANDARD'), ('PR', 'PREMIUM')], default='FREE', max_length=8, verbose_name='Тип подписки'),
        ),
    ]
