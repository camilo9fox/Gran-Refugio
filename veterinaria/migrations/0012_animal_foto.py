# Generated by Django 3.1.1 on 2020-12-15 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0011_remove_animal_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_pacientes', verbose_name='Foto'),
        ),
    ]
