from django.contrib import admin
from .models import TgUser, Message
from .utils import send_message
from django.shortcuts import render

@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'username', 'first_name', 'created_at')
    search_fields = ('chat_id', 'username', 'first_name')

    actions = ['send_distribution']

    def send_distribution(self, request, queryset):


        if 'broadcast_text' in request.POST:
            message_text = request.POST.get('broadcast_text', '')
            for user in queryset:
                send_message(user.chat_id, message_text) 

            self.message_user(request, f"Сообщение отправлено {queryset.count()} пользователям")
            return
        
        return render(request, 'bot/broadcast_form.html', {
            'users': queryset,
            'opts': self.model._meta,
        })


    send_distribution.short_description = "Разослать сообщение"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'is_bot', 'created_at')
    list_filter = ('is_bot', 'created_at')
    search_fields = ('text',)
