from django.urls import path
from . import views

app_name = 'heritage'

urlpatterns = [
    path('', views.patrimoine_list, name='list'),
    path('map/', views.patrimoine_map, name='map'),
    path('search/', views.patrimoine_search, name='search'),
    path('nearby/', views.patrimoine_nearby, name='nearby'),
    path('<int:pk>/', views.patrimoine_detail, name='detail'),
    path('create/', views.patrimoine_create, name='create'),
    path('<int:pk>/update/', views.patrimoine_update, name='update'),
    path('<int:pk>/delete/', views.patrimoine_delete, name='delete'),
]
