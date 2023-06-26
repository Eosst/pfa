from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from dashboard.models import Utilisateur

@receiver(post_save, sender=User)
def create_utilisateur(sender, instance, created, **kwargs):
    if created:
        Utilisateur.objects.create(user=instance)