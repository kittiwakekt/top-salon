from django.urls import path
from . import views

app_name = 'salon'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    
    # Поиск
    path('search/', views.search, name='search'),
    
    # Салоны
    path('salons/', views.SalonListView.as_view(), name='salon_list'),
    path('salons/<int:pk>/', views.SalonDetailView.as_view(), name='salon_detail'),
    path('salons/create/', views.SalonCreateView.as_view(), name='salon_create'),
    path('salons/<int:pk>/update/', views.SalonUpdateView.as_view(), name='salon_update'),
    path('salons/<int:pk>/delete/', views.SalonDeleteView.as_view(), name='salon_delete'),
    
    # Мастера
    path('masters/', views.MasterListView.as_view(), name='master_list'),
    path('masters/<int:pk>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('masters/create/', views.MasterCreateView.as_view(), name='master_create'),
    path('masters/<int:pk>/update/', views.MasterUpdateView.as_view(), name='master_update'),
    path('masters/<int:pk>/delete/', views.MasterDeleteView.as_view(), name='master_delete'),
    
    # Услуги
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    
    # Услуги мастеров
    path('master-services/create/', views.MasterServiceCreateView.as_view(), name='masterservice_create'),
    path('master-services/<int:pk>/update/', views.MasterServiceUpdateView.as_view(), name='masterservice_update'),
    path('master-services/<int:pk>/delete/', views.MasterServiceDeleteView.as_view(), name='masterservice_delete'),

]