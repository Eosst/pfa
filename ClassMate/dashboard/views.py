from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from datetime import date
from .forms import *
from .models import Absence, Etudiant, Filiere, Module, Promotion, Seance, Utilisateur
from django.core.paginator import Paginator

# Create your views here.
def Connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if(user is not None) and hasattr(user, 'utilisateur'):
            login(request, user)
            messages.success(request, "Vous avez été connecté avec succès")
            return redirect('/dashboard/')
        else:
            messages.error(request, "Le nom d'utilisateur ou le mot de passe est incorrect")
            return redirect('Connexion')
    else:
        return render(request, 'authentication/login.html', {})
def Deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès")
    return redirect('Connexion')

@login_required(login_url='Connexion')
def index(request):
    try:
        utilisateur = request.user.utilisateur 
    except AttributeError:
        messages.error(request, "vous etes pas un utilisateur, contactez l'administrateur")
        return redirect('Connexion')
    return render(request, 'dashboard/index.html', {'utilisateur':utilisateur, 'title':'Tableau de bord', })
def seances(request):
    utilisateur = request.user.utilisateur
    today = date.today()
    seances = Seance.objects.filter(Date=today)
    return render(request, 'dashboard/seances.html', {'utilisateur':utilisateur, 'title':'Séances', 'seances':seances})
def seances_manage(request):
    classes = []
    filieres = Filiere.objects.all()
    for filiere in filieres:
        promotions = Promotion.objects.filter(Filiere=filiere)
        promotions_data = [
            {"ID": promotion.ID, "Niveau": promotion.Niveau}
            for promotion in promotions
        ]
        classes.append({"filiere": {"ID": filiere.ID, "Nom": filiere.Nom}, "promotions": promotions_data})
    if request.method == 'POST' and 'promo_id' in request.POST:
        modules_data = []
        promo = Promotion.objects.get(ID=request.POST['promo_id'])
        if promo:
            return redirect('seances_manage', id=promo.ID)
    else:
        utilisateur = request.user.utilisateur
        return render(request, 'dashboard/seance_manage.html', {'utilisateur':utilisateur, 'title':'Gestion des séances', 'classes':classes})
def seances_manager(request, id):
    days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
    Types = ['Cours', 'TD', 'TP']
    utilisateur = request.user.utilisateur
    modules = Module.objects.filter(Promotion=id)
    classes = []
    filieres = Filiere.objects.all()
    enseignants = Utilisateur.objects.filter()
    for filiere in filieres:
        promotions = Promotion.objects.filter(Filiere=filiere)
        promotions_data = [
            {"ID": promotion.ID, "Niveau": dict(Promotion.NIVEAU_CHOICES).get(promotion.Niveau)}
            for promotion in promotions
        ]
        classes.append({"filiere": {"ID": filiere.ID, "Nom": filiere.Nom}, "promotions": promotions_data})

    # Check if the id is valid
    if Promotion.objects.filter(ID=id).exists():
        promo = Promotion.objects.get(ID=id)
        if request.method == 'POST':
            session_data = request.POST.dict()
            error_messages = []
            days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
            session_orders = ['1', '2', '3', '4']

            for day in days:
                for order in session_orders:
                    session_prefix = f"{day}_{order}"
                    module_key = f"module_{session_prefix}"
                    enseignant_key = f"enseignant_{session_prefix}"
                    type_key = f"type_{session_prefix}"

                    # Check if at least one element of the session is entered
                    if module_key in session_data or enseignant_key in session_data or type_key in session_data:
                        # Check if all elements of the session are present
                        if module_key not in session_data:
                            error_messages.append(f"Module manquant pour la séance {session_prefix}")
                        if enseignant_key not in session_data:
                            error_messages.append(f"Enseignant manquant pour la séance {session_prefix}")
                        if type_key not in session_data:
                            error_messages.append(f"Type manquant pour la séance {session_prefix}")

            if error_messages:
                response_data = {
                    'success': False,
                    'message': 'Erreur',
                    'errors': error_messages
                }
                return JsonResponse(response_data)
            else:
                table_data = []

                for day in days:
                    for order in session_orders:
                        session_prefix = f"{day}_{order}"
                        module = session_data.get(f"module_{session_prefix}")
                        enseignant = session_data.get(f"enseignant_{session_prefix}")
                        session_type = session_data.get(f"type_{session_prefix}")

                        # Exclude sessions with missing elements
                        if module is not None and enseignant is not None and session_type is not None:
                            table_data.append({
                                'jour': day,
                                'ordre_session': order,
                                'module': module,
                                'enseignant': enseignant,
                                'type': session_type
                            })

                response_data = {
                    'success': True,
                    'message': 'Succès',
                    'table_data': table_data
                }
                return JsonResponse(response_data)
        context = {
            'days': days,
            'sessions': [
                {'ID': 1, 'Heure': '08h30 - 10h30'},
                {'ID': 2, 'Heure': '10h45 - 12h45'},
                {'ID': 3, 'Heure': '14h30 - 16h30'},
                {'ID': 4, 'Heure': '16h45 - 18h45'},
            ],
            'Types': Types,
            'modules': modules,  # Remplacez par votre queryset de modules
            'enseignants': enseignants,  # Remplacez par votre queryset d'enseignants
            'classes': classes,
            'promo': promo,
            'utilisateur': utilisateur,
            'title': 'Gestion des séances',

        }
        return render(request, 'dashboard/seance_manage.html', context)
    else:
        messages.error(request, "La promotion n'existe pas")
        return redirect('seances_manage')
def filieres(request):
    form = FiliereForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "La filière a été ajoutée avec succès")
            return redirect('filieres') 
        else:
            error_message = form.errors.as_text()
            messages.error(request, error_message)
            return redirect('filieres')  
    else:
        utilisateur = request.user.utilisateur
        filieres = Filiere.objects.all()
        utilisateurs = Utilisateur.objects.filter(Role='Enseignant', filiere__isnull=True)
        return render(request, 'dashboard/filieres.html', {'utilisateur': utilisateur, 'title': 'Filières', 'filieres': filieres, 'utilisateurs': utilisateurs, 'form': form})
def etudiants(request):
    user = request.user
    utilisateur = user.utilisateur
    classes = []

    try:
        enseignant = Utilisateur.objects.get(User=user, Role=Utilisateur.ENSEIGNANT)

        seance_template_items = SeanceTemplateItem.objects.filter(enseignant=enseignant)

        for item in seance_template_items:
            seance_template = item.seance_template
            promotion = seance_template.promotion
            filiere = promotion.Filiere
            promotion_data = {"ID": promotion.ID, "Niveau": promotion.Niveau}
            filiere_data = {"ID": filiere.ID, "Nom": filiere.Nom}

            existing_filiere = next((item for item in classes if item["filiere"] == filiere_data), None)

            if existing_filiere:
                existing_filiere["promotions"].append(promotion_data)
            else:
                classes.append({"filiere": filiere_data, "promotions": [promotion_data]})

    except Utilisateur.DoesNotExist:
        filieres = Filiere.objects.all()

        for filiere in filieres:
            promotions = Promotion.objects.filter(Filiere=filiere)
            promotion_data = [{"ID": promotion.ID, "Niveau": promotion.Niveau} for promotion in promotions]
            filiere_data = {"ID": filiere.ID, "Nom": filiere.Nom}
            classes.append({"filiere": filiere_data, "promotions": promotion_data})
    return render(request, 'dashboard/etudiants.html', {'utilisateur':utilisateur, 'classes': classes, 'title': 'Etudiants'})
def absences(request):
    utilisateur = request.user.utilisateur
    absences = Absence.objects.all()
    return render(request, 'dashboard/absences.html', {'utilisateur':utilisateur, 'title':'Absences', 'absences':absences})
def absence_export(request):
    utilisateur = request.user.utilisateur
    absences = Absence.objects.all()
    return render(request, 'dashboard/absences.html', {'utilisateur':utilisateur, 'title':'Exportation des absences', 'absences':absences})
def modules(request):
    utilisateur = request.user.utilisateur
    modules_list = Module.objects.all()
    paginator = Paginator(modules_list, 10)  # Show 10 modules per page
    page_number = request.GET.get('page')
    modules = paginator.get_page(page_number)
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modules')  # Replace 'module_list' with your desired URL name for the module list view
    else:
        form = ModuleForm()

    context = {
        'utilisateur': utilisateur,
        'modules': modules,
        'title': 'Modules',
        'form': form,
    }

    return render(request, 'dashboard/modules.html', context)
def enseignants(request):
    utilisateur = request.user.utilisateur
    return render(request, 'dashboard/enseignants.html', {'utilisateur':utilisateur, 'title':'Enseignants', 'enseignants':utilisateur})
def promotions(request):
    utilisateur = request.user.utilisateur
    form = PromotionForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "La promotion a été ajoutée avec succès")
            return redirect('promotions') 
        else:
            messages.error(request, "Une erreur s'est produite lors de l'ajout de la promotion")
            return redirect('promotions')
    filieres = Filiere.objects.all()
    return render(request, 'dashboard/promotions.html', {'utilisateur':utilisateur, 'title':'Promotions', 'form':form, 'filieres':filieres})
def utilisateurs(request):
    utilisateur = request.user.utilisateur
    return render(request, 'dashboard/utilisateurs.html', {'utilisateur':utilisateur, 'title':'Utilisateurs', 'utilisateurs':utilisateur})
