from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from .models import Salon, Master, Service, MasterService
from .forms import MasterForm, ServiceForm, SalonForm, MasterServiceForm

# Salon Views
class SalonListView(ListView):
    model = Salon
    template_name = 'salon_list.html'
    context_object_name = 'salons'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Salon.objects.filter(is_active=True)
        return queryset

class SalonDetailView(DetailView):
    model = Salon
    template_name = 'salon_detail.html'
    context_object_name = 'salon'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = self.object.masters.filter(is_active=True)
        return context

class SalonCreateView(CreateView):
    model = Salon
    form_class = SalonForm
    template_name = 'salon_form.html'
    success_url = reverse_lazy('salon_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Салон успешно создан!')
        return super().form_valid(form)

class SalonUpdateView(UpdateView):
    model = Salon
    form_class = SalonForm
    template_name = 'salon_form.html'
    
    def get_success_url(self):
        return reverse_lazy('salon_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Салон успешно обновлен!')
        return super().form_valid(form)

class SalonDeleteView(DeleteView):
    model = Salon
    template_name = 'salon_confirm_delete.html'
    success_url = reverse_lazy('salon_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Салон успешно удален!')
        return super().delete(request, *args, **kwargs)

# Master Views
class MasterListView(ListView):
    model = Master
    template_name = 'master_list.html'
    context_object_name = 'masters'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Master.objects.filter(is_active=True).select_related('salon')
        
        # Фильтрация по специализации
        specialization = self.request.GET.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization=specialization)
        
        # Фильтрация по салону
        salon_id = self.request.GET.get('salon')
        if salon_id:
            queryset = queryset.filter(salon_id=salon_id)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(salon__name__icontains=search)
            )
        
        return queryset.order_by('-rating', 'last_name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['salons'] = Salon.objects.filter(is_active=True)
        context['specializations'] = Master.SPECIALIZATION_CHOICES
        return context

class MasterDetailView(DetailView):
    model = Master
    template_name = 'master_detail.html'
    context_object_name = 'master'
    
    def get_queryset(self):
        return Master.objects.select_related('salon').prefetch_related('master_services__service')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = self.object.master_services.filter(is_available=True)
        return context

class MasterCreateView(CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_form.html'
    success_url = reverse_lazy('master_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Мастер успешно добавлен!')
        return super().form_valid(form)

class MasterUpdateView(UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'master_form.html'
    
    def get_success_url(self):
        return reverse_lazy('master_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Данные мастера успешно обновлены!')
        return super().form_valid(form)

class MasterDeleteView(DeleteView):
    model = Master
    template_name = 'master_confirm_delete.html'
    success_url = reverse_lazy('master_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Мастер успешно удален!')
        return super().delete(request, *args, **kwargs)

# Service Views
class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'
    paginate_by = 15
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_available=True)
        
        # Фильтрация по категории
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Service.CATEGORY_CHOICES
        return context

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = MasterService.objects.filter(
            service=self.object, 
            is_available=True
        ).select_related('master')
        return context

class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = reverse_lazy('service_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Услуга успешно добавлена!')
        return super().form_valid(form)

class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    
    def get_success_url(self):
        return reverse_lazy('service_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Услуга успешно обновлена!')
        return super().form_valid(form)

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_confirm_delete.html'
    success_url = reverse_lazy('service_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Услуга успешно удалена!')
        return super().delete(request, *args, **kwargs)

# MasterService Views
class MasterServiceCreateView(CreateView):
    model = MasterService
    form_class = MasterServiceForm
    template_name = 'masterservice_form.html'
    
    def get_success_url(self):
        return reverse_lazy('master_detail', kwargs={'pk': self.object.master.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Услуга добавлена мастеру!')
        return super().form_valid(form)

class MasterServiceUpdateView(UpdateView):
    model = MasterService
    form_class = MasterServiceForm
    template_name = 'masterservice_form.html'
    
    def get_success_url(self):
        return reverse_lazy('master_detail', kwargs={'pk': self.object.master.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Услуга мастера обновлена!')
        return super().form_valid(form)

class MasterServiceDeleteView(DeleteView):
    model = MasterService
    template_name = 'masterservice_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('master_detail', kwargs={'pk': self.object.master.pk})
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Услуга удалена у мастера!')
        return super().delete(request, *args, **kwargs)

# Главная страница
def home(request):
    context = {
        'salons_count': Salon.objects.filter(is_active=True).count(),
        'masters_count': Master.objects.filter(is_active=True).count(),
        'services_count': Service.objects.filter(is_available=True).count(),
        'top_masters': Master.objects.filter(is_active=True).order_by('-rating')[:5],
        'popular_services': Service.objects.filter(is_available=True).annotate(
            masters_count=Count('service_masters')
        ).order_by('-masters_count')[:6],
    }
    return render(request, 'home.html', context)

# Поиск по всему
def search(request):
    query = request.GET.get('q', '')
    
    if query:
        masters = Master.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(salon__name__icontains=query),
            is_active=True
        ).select_related('salon')
        
        services = Service.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query),
            is_available=True
        )
        
        salons = Salon.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query),
            is_active=True
        )
    else:
        masters = Master.objects.none()
        services = Service.objects.none()
        salons = Salon.objects.none()
    
    context = {
        'query': query,
        'masters': masters,
        'services': services,
        'salons': salons,
    }
    
    return render(request, 'search_results.html', context)
