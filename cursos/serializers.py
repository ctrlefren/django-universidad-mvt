from rest_framework import serializers
from .models import Profesor, Estudiante, Curso

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    profesor_detalle = ProfesorSerializer(source='profesor', read_only=True)
    estudiantes_detalle = EstudianteSerializer(source='estudiantes', many=True, read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'codigo', 'profesor', 'profesor_detalle', 'estudiantes', 'estudiantes_detalle']