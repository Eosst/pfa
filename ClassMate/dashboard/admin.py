from django.contrib import admin

from .models import *

admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(Filiere)
admin.site.register(Promotion)
admin.site.register(Module)
admin.site.register(Seance)
admin.site.register(Absence)
admin.site.register(Justification)
admin.site.register(SeanceTemplateItem)
admin.site.register(SeanceTemplate)
