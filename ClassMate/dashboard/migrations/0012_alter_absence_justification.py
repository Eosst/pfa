# Generated by Django 4.2.1 on 2023-05-22 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_utilisateur_password_utilisateur_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absence',
            name='Justification',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.justification'),
        ),
    ]