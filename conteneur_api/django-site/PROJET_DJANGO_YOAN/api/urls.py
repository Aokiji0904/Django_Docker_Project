from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import PersonnageViewSet, ServeurViewSet, ClasseViewSet, NiveauViewSet, ContenuViewSet


   



router = DefaultRouter()
router.register(r'personnages', PersonnageViewSet) #endpoints de l'api
router.register(r'serveurs', ServeurViewSet)
router.register(r'niveaux', NiveauViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'contenus', ContenuViewSet)





urlpatterns = [
    path('importer-personnages/', views.importer_personnages, name='importer_personnages'),
    path('api/', include(router.urls)),  # Pour l'API REST
    

]


