# Generated by Django 3.1.1 on 2020-12-15 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0008_animal_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='foto',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='fotos_animales', verbose_name='Foto'),
        ),
    ]