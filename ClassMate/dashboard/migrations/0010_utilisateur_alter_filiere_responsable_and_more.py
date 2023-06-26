# Generated by Django 4.2.1 on 2023-05-22 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_filiere_responsable_alter_module_responsable_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('ID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('Nom', models.CharField(max_length=100)),
                ('Prenom', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100)),
                ('Role', models.CharField(choices=[('Enseignant', 'Enseignant'), ('Scolarite', 'Scolarite'), ('Admin', 'Admin')], max_length=100)),
                ('Password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='filiere',
            name='Responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.utilisateur'),
        ),
        migrations.AlterField(
            model_name='module',
            name='Responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.utilisateur'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='Utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.utilisateur'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='Enseignant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.utilisateur'),
        ),
    ]
