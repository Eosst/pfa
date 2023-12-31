# Generated by Django 4.2.1 on 2023-05-21 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_promotion_niveau'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='Promotion',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.promotion'),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='Delegue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.etudiant'),
        ),
    ]
