from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Salon(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название салона")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    opening_time = models.TimeField(verbose_name="Время открытия")
    closing_time = models.TimeField(verbose_name="Время закрытия")
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    def clean(self):
        if len(self.name) > 100:
            raise ValidationError('Используйте не более 100 символов')
        
    
    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"

    def __str__(self):
        return self.name

class Master(models.Model):
    SPECIALIZATION_CHOICES = [
        ('hair', 'Парикмахер'),
        ('nails', 'Маникюр'),
        ('cosmetology', 'Косметолог'),
        ('massage', 'Массажист'),
        ('barber', 'Барбер'),
    ]

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='masters', verbose_name="Салон")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, verbose_name="Специализация")
    experience = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Опыт работы (лет)")
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        verbose_name="Рейтинг"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    hire_date = models.DateField(verbose_name="Дата приема на работу")

    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"
        ordering = ['-rating', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_specialization_display()})"

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('hair', 'Волосы'),
        ('nails', 'Ногти'),
        ('face', 'Лицо'),
        ('body', 'Тело'),
        ('makeup', 'Макияж'),
    ]

    name = models.CharField(max_length=100, verbose_name="Название услуги")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    duration = models.IntegerField(validators=[MinValueValidator(5)], verbose_name="Длительность (мин)")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="Доступна")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name} - {self.price} руб."

class MasterService(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='master_services', verbose_name="Мастер")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_masters', verbose_name="Услуга")
    is_available = models.BooleanField(default=True, verbose_name="Доступна")
    special_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Специальная цена"
    )

    class Meta:
        verbose_name = "Услуга мастера"
        verbose_name_plural = "Услуги мастеров"
        unique_together = ['master', 'service']

    def get_price(self):
        return self.special_price if self.special_price else self.service.price

    def __str__(self):
        return f"{self.master} - {self.service}"