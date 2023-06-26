from django.http import HttpResponse
from django.urls import resolve
from dashboard.models import Utilisateur
from django.shortcuts import redirect
from django.contrib import messages as message

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.restricted_views = [
            'seances_manager',
            'seances_manage',
            'filieres',
            'promotions',
            'modules',
        ]

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)
       
        if request.user.is_superuser == True:
            return self.get_response(request)
        
        elif request.user.utilisateur.Role != Utilisateur.SCOLARITE and request.user.utilisateur.Role != Utilisateur.ADMIN:
            resolver_match = resolve(request.path_info)
            if resolver_match.view_name in self.restricted_views:
                message.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page")
                return redirect('index')

        return self.get_response(request)
