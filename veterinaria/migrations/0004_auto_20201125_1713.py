# Generated by Django 3.1.1 on 2020-11-25 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0003_auto_20201125_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rut',
            field=models.CharField(max_length=100, unique=True, verbose_name='Rut'),
        ),
    ]
