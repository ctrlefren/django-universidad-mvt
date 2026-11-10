from rest_framework.routers import DefaultRouter
from .api_views import CursoViewSet

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')

urlpatterns = router.urls