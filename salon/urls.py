# beauty/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    ServiceListView, ServiceDetailView, MasterListView, MasterDetailView,
    ClientDashboardView, CreateAppointmentView, ClientAppointmentHistoryView,
    CreateReviewView, MasterDashboardView, MasterScheduleView,
    MasterClientHistoryView, UpdateAppointmentStatusView,
    ClientProfileUpdateView
)

app_name = 'beauty'

urlpatterns = [
    # Public pages
    path('', ServiceListView.as_view(), name='service_list'),
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('masters/', MasterListView.as_view(), name='master_list'),
    path('masters/<int:pk>/', MasterDetailView.as_view(), name='master_detail'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='beauty:service_list'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # Client routes
    path('client/dashboard/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('client/appointment/create/', CreateAppointmentView.as_view(), name='create_appointment'),
    path('client/appointment/history/', ClientAppointmentHistoryView.as_view(), name='appointment_history'),
    path('client/review/create/', CreateReviewView.as_view(), name='create_review'),
    path('client/profile/update/', ClientProfileUpdateView.as_view(), name='update_client_profile'),
    
    # Master routes
    path('master/dashboard/', MasterDashboardView.as_view(), name='master_dashboard'),
    path('master/schedule/', MasterScheduleView.as_view(), name='master_schedule'),
    path('master/clients/<int:client_id>/', MasterClientHistoryView.as_view(), name='master_client_history'),
    path('master/appointment/<int:appointment_id>/update-status/', 
         UpdateAppointmentStatusView.as_view(), name='update_appointment_status'),
    
    # Administrator routes
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/appointments/', views.manage_appointments, name='manage_appointments'),
    path('admin/clients/', views.manage_clients, name='manage_clients'),
    path('admin/clients/<int:client_id>/', views.client_detail, name='client_detail'),
    
    # API endpoints
    path('api/master/<int:master_id>/schedule/', views.get_master_schedule, name='get_master_schedule'),
]