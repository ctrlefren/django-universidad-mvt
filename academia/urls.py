from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from cursos import views as cursos_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Página raíz: redirige al catálogo de cursos
    path('', RedirectView.as_view(pattern_name='web_lista_cursos', permanent=False)),

    # Endpoints de Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Enrutador de la API de Cursos
    path('api/', include('cursos.api_urls')),

    # Rutas web (vistas tradicionales con plantillas HTML)
    path('', include('cursos.urls')),

    # Rutas nativas de autenticación de Django (sesiones web)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]