# Generated by Django 3.1.1 on 2020-12-07 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinaria', '0005_auto_20201125_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(default='cliente', max_length=50, verbose_name='Tipo de usuario'),
        ),
    ]