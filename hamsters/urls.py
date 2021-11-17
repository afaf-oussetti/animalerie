from django.urls import path
from . import views


urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('animal/<str:id_animal>/', views.animal_detail, name='animal_detail'),
    path('deplacer_animal/<str:id_animal>', views.deplacer_animal, name='deplacer_animal'),
    path('deplacer_animal_litière/<str:id_animal>', views.deplacer_animal_litière, name='deplacer_animal_litière')
]