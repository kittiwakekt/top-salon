from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
import json

from .models import Service, Master, PortfolioItem, Client, Appointment, Review, WorkingHours
from .forms import AppointmentForm, ReviewForm, ClientProfileForm

# Utility functions for permission checks
def is_client(user):
    return hasattr(user, 'client') and user.is_authenticated

def is_master(user):
    return hasattr(user, 'master') and user.is_authenticated

def is_administrator(user):
    return user.is_staff or user.is_superuser

# Public views
class ServiceListView(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = self.object.masters.filter(is_active=True)
        return context

class MasterListView(ListView):
    model = Master
    template_name = 'masters/master_list.html'
    context_object_name = 'masters'
    
    def get_queryset(self):
        return Master.objects.filter(is_active=True).select_related('user')

class MasterDetailView(DetailView):
    model = Master
    template_name = 'masters/master_detail.html'
    context_object_name = 'master'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = self.object.portfolio.all()[:6]
        context['services'] = self.object.services.filter(is_active=True)
        context['reviews'] = Review.objects.filter(
            master=self.object, 
            is_approved=True
        )[:5]
        return context

# Client views
class ClientDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'clients/dashboard.html'
    
    def test_func(self):
        return is_client(self.request.user)
    
    def get(self, request):
        client = request.user.client
        appointments = Appointment.objects.filter(client=client).order_by('-appointment_date')
        context = {
            'client': client,
            'appointments': appointments,
            'upcoming_appointments': appointments.filter(
                appointment_date__gte=timezone.now()
            )[:5],
            'past_appointments': appointments.filter(
                appointment_date__lt=timezone.now()
            )[:10]
        }
        return render(request, self.template_name, context)

class CreateAppointmentView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'clients/create_appointment.html'
    success_url = reverse_lazy('client_dashboard')
    
    def test_func(self):
        return is_client(self.request.user)
    
    def form_valid(self, form):
        form.instance.client = self.request.user.client
        form.instance.status = 'pending'
        messages.success(self.request, 'Запись успешно создана! Ожидайте подтверждения.')
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.request.user.client
        return kwargs

class ClientAppointmentHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'clients/appointment_history.html'
    context_object_name = 'appointments'
    
    def test_func(self):
        return is_client(self.request.user)
    
    def get_queryset(self):
        return Appointment.objects.filter(
            client=self.request.user.client
        ).order_by('-appointment_date')

class CreateReviewView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'clients/create_review.html'
    success_url = reverse_lazy('client_dashboard')
    
    def test_func(self):
        return is_client(self.request.user)
    
    def form_valid(self, form):
        form.instance.client = self.request.user.client
        messages.success(self.request, 'Отзыв отправлен на модерацию!')
        return super().form_valid(form)

# Master views
class MasterDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'masters/dashboard.html'
    
    def test_func(self):
        return is_master(self.request.user)
    
    def get(self, request):
        master = request.user.master
        today = timezone.now().date()
        
        context = {
            'master': master,
            'today_appointments': Appointment.objects.filter(
                master=master,
                appointment_date__date=today,
                status__in=['confirmed', 'pending']
            ).order_by('appointment_date'),
            'upcoming_appointments': Appointment.objects.filter(
                master=master,
                appointment_date__date__gt=today,
                status__in=['confirmed', 'pending']
            ).order_by('appointment_date')[:10],
            'recent_appointments': Appointment.objects.filter(
                master=master,
                appointment_date__date__lt=today
            ).order_by('-appointment_date')[:10]
        }
        return render(request, self.template_name, context)

class MasterScheduleView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'masters/schedule.html'
    
    def test_func(self):
        return is_master(self.request.user)
    
    def get(self, request):
        master = request.user.master
        # Get appointments for the next 7 days
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=7)
        
        appointments = Appointment.objects.filter(
            master=master,
            appointment_date__date__range=[start_date, end_date]
        ).order_by('appointment_date')
        
        context = {
            'master': master,
            'appointments': appointments,
            'date_range': [start_date + timedelta(days=i) for i in range(7)]
        }
        return render(request, self.template_name, context)

class MasterClientHistoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'masters/client_history.html'
    
    def test_func(self):
        return is_master(self.request.user)
    
    def get(self, request, client_id):
        master = request.user.master
        client = get_object_or_404(Client, id=client_id)
        
        appointments = Appointment.objects.filter(
            master=master,
            client=client
        ).order_by('-appointment_date')
        
        context = {
            'client': client,
            'appointments': appointments
        }
        return render(request, self.template_name, context)

class UpdateAppointmentStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def test_func(self):
        return is_master(self.request.user)
    
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        # Check if the appointment belongs to this master
        if appointment.master != request.user.master:
            return HttpResponseForbidden()
        
        new_status = request.POST.get('status')
        if new_status in dict(Appointment.Status.choices):
            appointment.status = new_status
            appointment.save()
            messages.success(request, f'Статус записи обновлен на {appointment.get_status_display()}')
        else:
            messages.error(request, 'Неверный статус')
        
        return redirect('master_dashboard')

# Administrator views
@login_required
@user_passes_test(is_administrator)
def admin_dashboard(request):
    # Admin dashboard statistics
    today = timezone.now().date()
    
    context = {
        'total_appointments_today': Appointment.objects.filter(
            appointment_date__date=today
        ).count(),
        'pending_appointments': Appointment.objects.filter(
            status='pending'
        ).count(),
        'total_clients': Client.objects.count(),
        'total_masters': Master.objects.count(),
        'recent_appointments': Appointment.objects.select_related(
            'client', 'master', 'service'
        ).order_by('-created_at')[:10]
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_administrator)
def manage_appointments(request):
    appointments = Appointment.objects.select_related(
        'client', 'master', 'service'
    ).order_by('-appointment_date')
    
    status_filter = request.GET.get('status')
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_choices': Appointment.Status.choices
    }
    return render(request, 'admin/manage_appointments.html', context)

@login_required
@user_passes_test(is_administrator)
def manage_clients(request):
    clients = Client.objects.select_related('user').all()
    context = {'clients': clients}
    return render(request, 'admin/manage_clients.html', context)

@login_required
@user_passes_test(is_administrator)
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    appointments = Appointment.objects.filter(client=client).order_by('-appointment_date')
    reviews = Review.objects.filter(client=client)
    
    context = {
        'client': client,
        'appointments': appointments,
        'reviews': reviews
    }
    return render(request, 'admin/client_detail.html', context)

# API views for AJAX
@login_required
def get_master_schedule(request, master_id):
    if not (is_client(request.user) or is_master(request.user) or is_administrator(request.user)):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    master = get_object_or_404(Master, id=master_id)
    date_str = request.GET.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Get working hours for the day
    day_of_week = date.isoweekday()
    working_hours = WorkingHours.objects.filter(master=master, day_of_week=day_of_week).first()
    
    # Get appointments for the day
    appointments = Appointment.objects.filter(
        master=master,
        appointment_date__date=date,
        status__in=['confirmed', 'pending']
    )
    
    # Generate available time slots
    available_slots = []
    if working_hours and working_hours.is_working:
        current_time = datetime.combine(date, working_hours.start_time)
        end_time = datetime.combine(date, working_hours.end_time)
        
        while current_time + timedelta(minutes=30) <= end_time:
            slot_end = current_time + timedelta(minutes=30)
            
            # Check if slot is available
            is_available = not appointments.filter(
                appointment_date__lte=current_time,
                appointment_date__gte=slot_end - timedelta(minutes=30)
            ).exists()
            
            available_slots.append({
                'start': current_time.strftime('%H:%M'),
                'end': slot_end.strftime('%H:%M'),
                'available': is_available
            })
            
            current_time += timedelta(minutes=30)
    
    return JsonResponse({
        'working_hours': {
            'start': working_hours.start_time.strftime('%H:%M') if working_hours else None,
            'end': working_hours.end_time.strftime('%H:%M') if working_hours else None,
            'is_working': working_hours.is_working if working_hours else False
        },
        'available_slots': available_slots
    })

# Profile views
@login_required
def profile_view(request):
    user = request.user
    
    if is_client(user):
        return redirect('client_dashboard')
    elif is_master(user):
        return redirect('master_dashboard')
    elif is_administrator(user):
        return redirect('admin_dashboard')
    else:
        return redirect('service_list')

class ClientProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientProfileForm
    template_name = 'clients/update_profile.html'
    success_url = reverse_lazy('client_dashboard')
    
    def test_func(self):
        return is_client(self.request.user)
    
    def get_object(self):
        return self.request.user.client