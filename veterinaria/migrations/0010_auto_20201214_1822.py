# Generated by Django 3.1.1 on 2020-12-15 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0009_auto_20201214_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_animales', verbose_name='Foto'),
        ),
    ]
