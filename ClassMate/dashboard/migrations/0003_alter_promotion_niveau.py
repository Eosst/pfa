# Generated by Django 4.2.1 on 2023-05-21 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_utilisateur_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='Niveau',
            field=models.CharField(choices=[('1ere annee', '1ere annee'), ('2eme annee', '2eme annee'), ('3eme annee', '3eme annee'), ('4eme annee', '4eme annee'), ('5eme annee', '5eme annee')], max_length=100),
        ),
    ]
