from django.contrib import admin
from .models import Profesor, Curso, Estudiante


@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'especialidad')
    list_filter = ('especialidad',)
    search_fields = ('nombre', 'email', 'especialidad')


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nombre', 'email')
    search_fields = ('matricula', 'nombre', 'email')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'profesor')
    list_filter = ('profesor',)
    search_fields = ('codigo', 'nombre', 'profesor__nombre')
    filter_horizontal = ('estudiantes',)
    