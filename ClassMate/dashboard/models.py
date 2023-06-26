from django.db import models
from django.contrib.auth.models import User

class Utilisateur(models.Model):
    ENSEIGNANT = 'Enseignant'
    SCOLARITE = 'Scolarite'
    ADMIN = 'Admin'

    ROLE_CHOICES = (
        (ENSEIGNANT, 'Enseignant'),
        (SCOLARITE, 'Scolarite'),
        (ADMIN, 'Admin'),
    )
    User = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    ID = models.CharField(max_length=100, primary_key=True)
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"
class Etudiant(models.Model):
    Apogee = models.CharField(max_length=100, primary_key=True)
    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Promotion = models.ForeignKey('Promotion', on_delete=models.SET_NULL , default=None, null=True, blank=True)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"
class Filiere(models.Model):
    ID = models.CharField(max_length=100, primary_key=True)
    Nom = models.CharField(max_length=100)
    Responsable = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    def __str__(self):
        return self.Nom
class Promotion(models.Model):
    FIRST_YEAR = '1A'
    SECOND_YEAR = '2A'
    THIRD_YEAR = '3A'
    FOURTH_YEAR = '4A'
    FIFTH_YEAR = '5A'

    NIVEAU_CHOICES = (
        (FIRST_YEAR, '1ère année'),
        (SECOND_YEAR, '2ème année'),
        (THIRD_YEAR, '3ème année'),
        (FOURTH_YEAR, '4ème année'),
        (FIFTH_YEAR, '5ème année'),
    )
    ID = models.CharField(max_length=100, primary_key=True)
    Niveau = models.CharField(max_length=100 , choices=NIVEAU_CHOICES)
    Filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    Delegue = models.ForeignKey(Etudiant, on_delete=models.SET_NULL, null=True , default=None, blank=True)
    def __str__(self):
        return str(self.ID)
class Module(models.Model):
    ID = models.CharField(max_length=100, primary_key=True)
    Nom = models.CharField(max_length=100)
    Responsable = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    Promotion = models.ManyToManyField(Promotion)
    def __str__(self):
        return self.Nom
class Seance(models.Model):
    ID = models.AutoField(primary_key=True)
    SEANCE1 = '8h30 - 10h30'
    SEANCE2 = '10h45 - 12h45'
    SEANCE3 = '14h30 - 16h30'
    SEANCE4 = '16h45 - 18h45'
    SEANCE_CHOICES = (
        (SEANCE1, '8h30 - 10h30'),
        (SEANCE2, '10h45 - 12h45'),
        (SEANCE3, '14h30 - 16h30'),
        (SEANCE4, '16h45 - 18h45'),
    )
    COURS = 'Cours'
    TD = 'TD'
    TP = 'TP'
    Type_CHOICES = (
        (COURS, 'Cours'),
        (TD, 'TD'),
        (TP, 'TP'),
    )
    
    Ordre = models.CharField(max_length=100 , choices=SEANCE_CHOICES)
    Type = models.CharField(max_length=100 , choices=Type_CHOICES)
    Module = models.ForeignKey(Module, on_delete=models.CASCADE)
    Enseignant = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    Promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True)
    Date = models.DateField()
    def __str__(self):
        return str(self.Module )+ " - " + str(self.Type) + " - " + str(self.Date)
class Absence(models.Model):
    ID = models.AutoField(primary_key=True)
    Etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    Seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    Justification = models.OneToOneField('Justification', on_delete=models.CASCADE, null=True , default=None, blank=True)
    def __str__(self):
        return str(self.Etudiant) + " - " + str(self.Seance)
class Justification(models.Model):
    ID = models.AutoField(primary_key=True)
    Justifiee = models.BooleanField(default=False)
    Justification = models.CharField(max_length=100 , null=True , blank=True)
    Date = models.DateField()
    def __str__(self):
        if self.Justifiee:
            return "Justifiee"
        else:
            return "Non Justifiee"
class Notification(models.Model):
    ID = models.AutoField(primary_key=True)
    Contenu = models.CharField(max_length=100)
    Date = models.DateField()
    Utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    Seen = models.BooleanField(default=False)
    def __str__(self):
        return self.Utilisateur + " - " + self.Date
class SeanceTemplate(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

class SeanceTemplateItem(models.Model):
    SEANCE1 = '8h30 - 10h30'
    SEANCE2 = '10h45 - 12h45'
    SEANCE3 = '14h30 - 16h30'
    SEANCE4 = '16h45 - 18h45'
    SEANCE_CHOICES = (
        (SEANCE1, '8h30 - 10h30'),
        (SEANCE2, '10h45 - 12h45'),
        (SEANCE3, '14h30 - 16h30'),
        (SEANCE4, '16h45 - 18h45'),
    )
    COURS = 'Cours'
    TD = 'TD'
    TP = 'TP'
    Type_CHOICES = (
        (COURS, 'Cours'),
        (TD, 'TD'),
        (TP, 'TP'),
    )
    seance_template = models.ForeignKey(SeanceTemplate, on_delete=models.CASCADE)
    jour = models.CharField(max_length=100)
    session = models.CharField(max_length=100 , choices=SEANCE_CHOICES)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    type_seance = models.CharField(max_length=100 , choices=Type_CHOICES)