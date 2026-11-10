from django import forms
from .models import Curso, Estudiante

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'codigo', 'profesor', 'estudiantes']
        labels = {
            'nombre': 'Nombre del Curso',
            'codigo': 'Código Único',
            'profesor': 'Profesor Asignado (ForeignKey)',
            'estudiantes': 'Estudiantes Inscritos (ManyToManyField)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Programación Python'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. PY101'}),
            'profesor': forms.Select(attrs={'class': 'form-select'}),
            'estudiantes': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].upper()
        if len(codigo) < 4:
            raise forms.ValidationError('El código debe tener al menos 4 caracteres.')
        return codigoS

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'email', 'matricula']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
        }