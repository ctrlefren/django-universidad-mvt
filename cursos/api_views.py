from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Curso
from .serializers import CursoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

    # Permite lectura pública (GET), pero exige token para POST, PUT, DELETE
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]