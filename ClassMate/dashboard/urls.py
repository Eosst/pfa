from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('dashboard/', views.index, name='index'),
    # seances

    path('dashboard/seances/', views.seances, name='seances'),
    path('dashboard/seances/manage/', views.seances_manage, name='seances_manage'),
    # with an id as string parameter
    path('dashboard/seances/manage/<str:id>/', views.seances_manager, name='seances_manage'),
    # filieres

    path('dashboard/filieres/', views.filieres, name='filieres'),
   
    # etudiants

    path('dashboard/etudiants/', views.etudiants, name='etudiants'),
    
    # absences

    path('dashboard/absences/', views.absences, name='absences'),

    # absences list export

    path('dashboard/absences/export/', views.absence_export, name='absences_export'),
    
    # modules

    path('dashboard/modules/', views.modules, name='modules'),
    
    # enseignants

    path('dashboard/enseignants/', views.enseignants, name='enseignants'),
    
    # promotions

    path('dashboard/promotions/', views.promotions, name='promotions'),
    
    # utilisateurs

    path('dashboard/utilisateurs/', views.utilisateurs, name='utilisateurs'),
    

    path('connexion/', views.Connexion, name='Connexion'),
    path('deconnexion/', views.Deconnexion, name='Deconnexion')
]