# Generated by Django 4.2.1 on 2023-05-21 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_promotion_delegue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='Ordre',
            field=models.CharField(choices=[('8h30 - 10h30', '8h30 - 10h30'), ('10h45 - 12h45', '10h45 - 12h45'), ('14h30 - 16h30', '14h30 - 16h30'), ('16h45 - 18h45', '16h45 - 18h45')], max_length=100),
        ),
        migrations.AlterField(
            model_name='seance',
            name='Type',
            field=models.CharField(choices=[('Cours', 'Cours'), ('TD', 'TD'), ('TP', 'TP')], max_length=100),
        ),
    ]
