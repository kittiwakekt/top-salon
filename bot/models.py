from django.db import models
from django_fsm import FSMField, transition
from salon.models import Master, Salon
from datetime import datetime


class TgUser(models.Model):
    """Модель для хранения пользователя Telegram"""
    chat_id = models.BigIntegerField(unique=True, verbose_name="ID чата")
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первого сообщения")
    
    STATE_CHOICES = [
        ('start', 'Старт'),
        ('wating_master_first_name', 'Ожидание имени мастера'),
        ('wating_master_last_name', 'Ожидание фамилии мастера'),
        ('wating_specialization', 'Ожидание специализации'),
        ('wating_experience', 'Ожидание опыта мастера'),
        ('wating_salon', 'Ожидание номера салона'),
    ]
    state = FSMField(
        choices=STATE_CHOICES,
        default='start',
        protected=True,
        verbose_name="Состояние диалога"
    )
    context = models.JSONField(null=True, blank=True, verbose_name="Контекст диалога")

    @transition(field=state, source='start', target='wating_master_first_name')
    def start_adding_master(self):
        """Начало процесса добавления мастера"""
        pass

    @transition(field=state, source='wating_master_first_name', target='wating_master_last_name')
    def set_master_name(self, name: str):
        """Сохранение имени мастера и переход к следующему шагу"""
        self.context = {'first_name': name}
        self.save()

    @transition(field=state, source='wating_master_last_name', target='wating_specialization')
    def set_master_last_name(self, name: str):
        """Сохранение фамилии мастера и переход к следующему шагу"""
        cont = self.context
        cont['last_name'] = name
        self.context = cont
        self.save()

    @transition(field=state, source='wating_specialization', target='wating_experience')
    def set_master_specialization(self, specialization: str):
        """Сохранение фамилии специализации и переход к следующему шагу"""

        spec = dict([
            ('Парикмахер', 'hair'),
            ('Маникюр', 'nails'),
            ('Косметолог', 'cosmetology'),
            ('Массажист', 'massage'),
            ('Барбер', 'barber')
        ])
        self.context['specialization'] = spec.get(specialization,'hair')
        self.save()

    @transition(field=state, source='wating_experience', target='wating_salon')
    def set_master_experience(self, experience: int):
        """Сохранение специализации и переход к следующему шагу"""
        self.context['experience'] = experience
        self.save()

    @transition(field=state, source='wating_salon', target='start')
    def set_master_salon(self, salon_id: int):
        """Сохранение salon и завершение диалога"""
        salon = Salon.objects.get(id=salon_id)
        master = Master.objects.create(
            salon = salon,
            first_name = self.context.get('first_name'),
            last_name = self.context.get('last_name'),
            specialization = self.context.get('specialization'),
            experience = self.context.get('experience'),
            hire_date = datetime.today()
        )
        self.context = {}
        self.save()
        
        
    def reset_state(self):
        """Сброс состояния в начальное (для команды /cancel)"""
        self.state = 'start'
        self.context = {}
        self.save()



    def __str__(self):
        return f"{self.username or self.first_name} ({self.chat_id})"

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"


class Message(models.Model):
    """Модель для логирования всех сообщений (для истории и аналитики)"""
    user = models.ForeignKey(TgUser, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField(verbose_name="Текст сообщения")
    is_bot = models.BooleanField(default=False, verbose_name="Отправлено ботом?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.text[:20]}..."

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"