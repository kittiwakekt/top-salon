from django.contrib import admin
from django.utils.html import format_html
from .models import Salon, Master, Service, MasterService

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'opening_time', 'closing_time', 'is_active', 'masters_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'address', 'phone')
    list_editable = ('is_active',)
    
    def masters_count(self, obj):
        return obj.masters.count()
    masters_count.short_description = 'Количество мастеров'

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'salon', 'specialization', 'experience', 'rating', 'is_active', 'hire_date', 'services_count')
    list_filter = ('specialization', 'is_active', 'salon', 'hire_date')
    search_fields = ('first_name', 'last_name', 'salon__name')
    list_editable = ('is_active', 'rating')
    readonly_fields = ('hire_date',)
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Мастер'
    
    def services_count(self, obj):
        return obj.master_services.count()
    services_count.short_description = 'Количество услуг'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'duration', 'price', 'is_available', 'masters_count')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'price')
    
    def masters_count(self, obj):
        return obj.service_masters.count()
    masters_count.short_description = 'Количество мастеров'

@admin.register(MasterService)
class MasterServiceAdmin(admin.ModelAdmin):
    list_display = ('master', 'service', 'get_price_display', 'is_available')
    list_filter = ('is_available', 'master__specialization', 'service__category')
    search_fields = ('master__first_name', 'master__last_name', 'service__name')
    list_editable = ('is_available',)
    autocomplete_fields = ('master', 'service')
    
    actions = ['action_activate', 'action_deactivate']

    def get_price_display(self, obj):
        price = obj.get_price()
        if obj.special_price:
            return format_html(
                '<span style="color: green; text-decoration: line-through;">{}</span> <span style="color: red;">{}</span>',
                obj.service.price,
                price
            )
        return f"{price} руб."
    get_price_display.short_description = 'Цена'

    def action_activate(self, request, queryset):
        """Активировать выбранных услуг мастеров"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f"Активировано {updated} услуг мастеров")
    action_activate.short_description = "Активировать выбранные услуги мастеров"

    def action_deactivate(self, request, queryset):
        """Деактивировать выбранных услуг мастеров"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f"Деактивировано {updated} услуг мастеров")
    action_deactivate.short_description = "Деактивировать выбранные услуги мастеров"
