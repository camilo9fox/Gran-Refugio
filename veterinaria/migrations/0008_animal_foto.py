# Generated by Django 3.1.1 on 2020-12-15 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0007_animal'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='foto',
            field=models.ImageField(default=None, upload_to='fotos_animales', verbose_name='Foto'),
        ),
    ]