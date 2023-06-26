from django import forms
from .models import Filiere, Utilisateur, Promotion, Module, Seance, Etudiant, Absence, SeanceTemplateItem, SeanceTemplate, Justification
from django.forms import formset_factory

class FiliereForm(forms.ModelForm):
    Responsable = forms.ModelChoiceField(queryset=Utilisateur.objects.filter(Role='Enseignant', filiere__isnull=True))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Responsable'].queryset = Utilisateur.objects.filter(Role='Enseignant', filiere__isnull=True)

    def clean_Responsable(self):
        responsable = self.cleaned_data.get('Responsable')
        if responsable is not None and not Utilisateur.objects.filter(pk=responsable.pk, Role='Enseignant', filiere__isnull=True).exists():
            raise forms.ValidationError("Invalid selection for the Responsable field.")
        return responsable

    class Meta:
        model = Filiere
        fields = ['ID', 'Nom', 'Responsable']
        widgets = {
            'ID': forms.TextInput(attrs={'class': 'form-control'}),
            'Nom': forms.TextInput(attrs={'class': 'form-control'}),
            'Responsable': forms.Select(attrs={'class': 'form-control'}),
        }
class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['Filiere', 'Niveau', 'Delegue']
        widgets = {
            'Filiere': forms.Select(attrs={'class': 'form-control'}),
            'Niveau': forms.Select(attrs={'class': 'form-control'}),
            'Delegue': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Delegue'].queryset = Etudiant.objects.exclude(promotion__isnull=False)

    def clean(self):
        cleaned_data = super().clean()
        filiere = cleaned_data.get('Filiere')
        niveau = cleaned_data.get('Niveau')
        delegue = cleaned_data.get('Delegue')

        if filiere and delegue:
            existing_promotions = Promotion.objects.filter(Filiere=filiere, Delegue=delegue)
            if existing_promotions.exists():
                raise forms.ValidationError("Le même délégué est déjà associé à une autre promotion.")

        if filiere and niveau:
            existing_levels = Promotion.objects.filter(Filiere=filiere, Niveau__startswith=niveau[0])
            if existing_levels.exists():
                raise forms.ValidationError("La même filière a déjà une promotion avec le même niveau.")

        return cleaned_data


    def save(self, commit=True):
        instance = super().save(commit=False)
        niveau = self.cleaned_data['Niveau']
        level = niveau[0] if niveau else None
        instance.ID = f"{instance.Filiere.ID}{level}"
        if commit:
            instance.save()
        return instance



class SeanceManagerForm(forms.Form):
    def __init__(self, days, sessions, modules, enseignants, *args, **kwargs):
        super(SeanceManagerForm, self).__init__(*args, **kwargs)
        self.days = days
        self.sessions = sessions
        self.modules = modules
        self.enseignants = enseignants
        self.initialize_fields()

    def initialize_fields(self):
        for day in self.days:
            for session in self.sessions:
                module_field_name = f"module_{day}_{session}"
                enseignant_field_name = f"enseignant_{day}_{session}"
                module_choices = [(module.ID, module.Nom) for module in self.modules]
                enseignant_choices = [(enseignant.ID, f"{enseignant.Nom} {enseignant.Prenom}") for enseignant in self.enseignants]
                self.fields[module_field_name] = forms.ChoiceField(
                    choices=[("", "Module")] + module_choices,
                    widget=forms.Select(attrs={"class": "form-control mb-1"})
                )
                self.fields[enseignant_field_name] = forms.ChoiceField(
                    choices=[("", "Enseignant")] + enseignant_choices,
                    widget=forms.Select(attrs={"class": "form-control"})
                )

    def clean(self):
        cleaned_data = super().clean()
        for day in self.days:
            for session in self.sessions:
                module_field_name = f"module_{day}_{session}"
                enseignant_field_name = f"enseignant_{day}_{session}"
                module = cleaned_data.get(module_field_name)
                enseignant = cleaned_data.get(enseignant_field_name)
                if module and not enseignant:
                    self.add_error(enseignant_field_name, "An enseignant must be selected if a module is chosen.")

        return cleaned_data
class ModuleForm(forms.ModelForm):
    Promotion = forms.ModelMultipleChoiceField(
        queryset=Promotion.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'rows': '5'}),
        to_field_name='ID'
    )

    class Meta:
        model = Module
        fields = ['ID', 'Nom', 'Responsable', 'Promotion']
        widgets = {
            'ID': forms.TextInput(attrs={'class': 'form-control'}),
            'Nom': forms.TextInput(attrs={'class': 'form-control'}),
            'Responsable': forms.Select(attrs={'class': 'form-control'}),
        }
class SeanceTemplateItemForm(forms.ModelForm):
    class Meta:
        model = SeanceTemplateItem
        fields = ['jour', 'session', 'module', 'enseignant', 'type_seance']
        widgets = {
            'jour': forms.HiddenInput(),
            'session': forms.HiddenInput(),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'type_seance': forms.Select(attrs={'class': 'form-control'}),
        }
days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
sessions = {
        1: '8h30 - 10h30',
        2: '10h45 - 12h45',
        3: '14h30 - 14h30',
        4: '16h45 - 18h45',
    }
Types = ['Cours', 'TD', 'TP']
SeanceTemplateItemFormSet = formset_factory(
    SeanceTemplateItemForm,
    extra=len(days) * len(sessions),
    max_num=len(days) * len(sessions),
    validate_max=True
)