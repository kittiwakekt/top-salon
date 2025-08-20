from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import os

def service_image_path(instance, filename):
    return f'services/{instance.id}/{filename}'

def master_photo_path(instance, filename):
    return f'masters/{instance.id}/photos/{filename}'

def portfolio_image_path(instance, filename):
    return f'portfolio/{instance.master.id}/{filename}'

class Service(models.Model):
    """Модель услуги салона"""
    name = models.CharField(max_length=200, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    duration = models.DurationField(verbose_name="Длительность")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to=service_image_path, null=True, blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Master(models.Model):
    """Модель мастера"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    services = models.ManyToManyField(Service, related_name='masters', verbose_name="Услуги")
    experience = models.PositiveIntegerField(verbose_name="Опыт работы (лет)", default=0)
    description = models.TextField(verbose_name="О мастере", blank=True)
    photo = models.ImageField(upload_to=master_photo_path, null=True, blank=True, verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    specialization = models.CharField(max_length=200, verbose_name="Специализация")
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

class PortfolioItem(models.Model):
    """Модель работы в портфолио мастера"""
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='portfolio', verbose_name="Мастер")
    image = models.ImageField(upload_to=portfolio_image_path, verbose_name="Фото работы")
    description = models.TextField(verbose_name="Описание работы", blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Работа в портфолио"
        verbose_name_plural = "Портфолио"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.master} - {self.service}"

class Client(models.Model):
    """Модель клиента"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.phone})"

class Appointment(models.Model):
    """Модель записи на процедуру"""
    
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Подтверждена'
        COMPLETED = 'completed', 'Завершена'
        CANCELLED = 'cancelled', 'Отменена'
        PENDING = 'pending', 'Ожидание'
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING,
        verbose_name="Статус"
    )
    notes = models.TextField(blank=True, verbose_name="Заметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ['-appointment_date']
        unique_together = ['master', 'appointment_date']
    
    def __str__(self):
        return f"{self.client} - {self.service} - {self.appointment_date}"

class Review(models.Model):
    """Модель отзыва"""
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    master = models.ForeignKey(Master, on_delete=models.CASCADE, verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрен")
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
        unique_together = ['client', 'master', 'service']
    
    def __str__(self):
        return f"{self.client} - {self.master} - {self.rating} звезд"

class WorkingHours(models.Model):
    """Модель рабочих часов мастера"""
    
    class DayOfWeek(models.IntegerChoices):
        MONDAY = 1, 'Понедельник'
        TUESDAY = 2, 'Вторник'
        WEDNESDAY = 3, 'Среда'
        THURSDAY = 4, 'Четверг'
        FRIDAY = 5, 'Пятница'
        SATURDAY = 6, 'Суббота'
        SUNDAY = 7, 'Воскресенье'
    
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='working_hours', verbose_name="Мастер")
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, verbose_name="День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    is_working = models.BooleanField(default=True, verbose_name="Рабочий день")
    
    class Meta:
        verbose_name = "Рабочее время"
        verbose_name_plural = "Рабочее время"
        unique_together = ['master', 'day_of_week']
        ordering = ['day_of_week']
    
    def __str__(self):
        return f"{self.master} - {self.get_day_of_week_display()}"