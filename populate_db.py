# populate_db.py
import os
import django
from datetime import date, time
from decimal import Decimal

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from salon.models import Salon, Master, Service, MasterService

def create_salons():
    """Создание салонов"""
    salons_data = [
        {
            'name': 'Элит Красота',
            'address': 'ул. Центральная, 15',
            'phone': '+7 (495) 123-45-67',
            'opening_time': time(9, 0),
            'closing_time': time(21, 0),
            'is_active': True
        },
        {
            'name': 'Стиль и Гармония',
            'address': 'пр. Победы, 28',
            'phone': '+7 (495) 987-65-43',
            'opening_time': time(10, 0),
            'closing_time': time(20, 0),
            'is_active': True
        },
        {
            'name': 'Люкс Причесок',
            'address': 'ул. Садовая, 7',
            'phone': '+7 (495) 555-44-33',
            'opening_time': time(8, 0),
            'closing_time': time(22, 0),
            'is_active': True
        }
    ]
    
    salons = []
    for data in salons_data:
        salon, created = Salon.objects.get_or_create(**data)
        salons.append(salon)
        print(f'Создан салон: {salon.name}')
    
    return salons

def create_services():
    """Создание услуг"""
    services_data = [
        # Волосы
        {'name': 'Женская стрижка', 'category': 'hair', 'duration': 60, 'price': 1500, 'description': 'Стрижка с укладкой'},
        {'name': 'Мужская стрижка', 'category': 'hair', 'duration': 45, 'price': 800, 'description': 'Стрижка машинкой и ножницами'},
        {'name': 'Окрашивание волос', 'category': 'hair', 'duration': 120, 'price': 3000, 'description': 'Полное окрашивание'},
        {'name': 'Мелирование', 'category': 'hair', 'duration': 180, 'price': 4500, 'description': 'Частичное мелирование'},
        {'name': 'Укладка', 'category': 'hair', 'duration': 30, 'price': 700, 'description': 'Вечерняя укладка'},
        
        # Ногти
        {'name': 'Маникюр классический', 'category': 'nails', 'duration': 60, 'price': 1200, 'description': 'Обрезной маникюр'},
        {'name': 'Педикюр', 'category': 'nails', 'duration': 90, 'price': 2000, 'description': 'Комплексный педикюр'},
        {'name': 'Наращивание ногтей', 'category': 'nails', 'duration': 120, 'price': 3500, 'description': 'Гелевое наращивание'},
        {'name': 'Покрытие гель-лаком', 'category': 'nails', 'duration': 45, 'price': 1000, 'description': 'С покрытием базой и топом'},
        
        # Лицо
        {'name': 'Чистка лица', 'category': 'face', 'duration': 90, 'price': 2500, 'description': 'Механическая чистка'},
        {'name': 'Уходовая процедура', 'category': 'face', 'duration': 60, 'price': 1800, 'description': 'Увлажняющая процедура'},
        {'name': 'Пилинг', 'category': 'face', 'duration': 45, 'price': 1500, 'description': 'Химический пилинг'},
        
        # Тело
        {'name': 'Расслабляющий массаж', 'category': 'body', 'duration': 60, 'price': 2000, 'description': 'Общий массаж тела'},
        {'name': 'Антицеллюлитный массаж', 'category': 'body', 'duration': 90, 'price': 3000, 'description': 'Курс из 10 процедур'},
        {'name': 'Обертывание', 'category': 'body', 'duration': 60, 'price': 2500, 'description': 'Шоколадное обертывание'},
        
        # Макияж
        {'name': 'Дневной макияж', 'category': 'makeup', 'duration': 45, 'price': 1500, 'description': 'Естественный макияж'},
        {'name': 'Вечерний макияж', 'category': 'makeup', 'duration': 60, 'price': 2500, 'description': 'Смоки айс'},
        {'name': 'Свадебный макияж', 'category': 'makeup', 'duration': 90, 'price': 5000, 'description': 'С пробой и консультацией'},
    ]
    
    services = []
    for data in services_data:
        service, created = Service.objects.get_or_create(**data)
        services.append(service)
        print(f'Создана услуга: {service.name}')
    
    return services

def create_masters(salons):
    """Создание мастеров"""
    masters_data = [
        # Салон 1 - Элит Красота
        {
            'salon': salons[0],
            'first_name': 'Анна',
            'last_name': 'Иванова',
            'specialization': 'hair',
            'experience': 8,
            'rating': 4.8,
            'is_active': True,
            'hire_date': date(2018, 3, 15)
        },
        {
            'salon': salons[0],
            'first_name': 'Мария',
            'last_name': 'Петрова',
            'specialization': 'nails',
            'experience': 5,
            'rating': 4.7,
            'is_active': True,
            'hire_date': date(2019, 6, 10)
        },
        {
            'salon': salons[0],
            'first_name': 'Ольга',
            'last_name': 'Сидорова',
            'specialization': 'cosmetology',
            'experience': 10,
            'rating': 4.9,
            'is_active': True,
            'hire_date': date(2016, 1, 20)
        },
        
        # Салон 2 - Стиль и Гармония
        {
            'salon': salons[1],
            'first_name': 'Екатерина',
            'last_name': 'Смирнова',
            'specialization': 'hair',
            'experience': 6,
            'rating': 4.6,
            'is_active': True,
            'hire_date': date(2019, 9, 5)
        },
        {
            'salon': salons[1],
            'first_name': 'Дарья',
            'last_name': 'Кузнецова',
            'specialization': 'massage',
            'experience': 4,
            'rating': 4.5,
            'is_active': True,
            'hire_date': date(2020, 2, 18)
        },
        {
            'salon': salons[1],
            'first_name': 'Иван',
            'last_name': 'Попов',
            'specialization': 'barber',
            'experience': 7,
            'rating': 4.7,
            'is_active': True,
            'hire_date': date(2018, 11, 30)
        },
        
        # Салон 3 - Люкс Причесок
        {
            'salon': salons[2],
            'first_name': 'Светлана',
            'last_name': 'Васильева',
            'specialization': 'hair',
            'experience': 12,
            'rating': 4.9,
            'is_active': True,
            'hire_date': date(2015, 5, 12)
        },
        {
            'salon': salons[2],
            'first_name': 'Наталья',
            'last_name': 'Федорова',
            'specialization': 'makeup',
            'experience': 8,
            'rating': 4.8,
            'is_active': True,
            'hire_date': date(2017, 8, 22)
        },
        {
            'salon': salons[2],
            'first_name': 'Александр',
            'last_name': 'Морозов',
            'specialization': 'barber',
            'experience': 9,
            'rating': 4.8,
            'is_active': True,
            'hire_date': date(2016, 12, 3)
        }
    ]
    
    masters = []
    for data in masters_data:
        master, created = Master.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            defaults=data
        )
        masters.append(master)
        print(f'Создан мастер: {master.first_name} {master.last_name}')
    
    return masters

def assign_services_to_masters(masters, services):
    """Назначение услуг мастерам"""
    # Распределение услуг по специализациям
    specialization_services = {
        'hair': [s for s in services if s.category == 'hair'],
        'nails': [s for s in services if s.category == 'nails'],
        'cosmetology': [s for s in services if s.category == 'face'],
        'massage': [s for s in services if s.category == 'body'],
        'barber': [s for s in services if s.name in ['Мужская стрижка']],
        'makeup': [s for s in services if s.category == 'makeup']
    }
    
    master_services_created = 0
    
    for master in masters:
        # Получаем услуги для специализации мастера
        master_services = specialization_services.get(master.specialization, [])
        
        for service in master_services:
            # Для некоторых мастеров устанавливаем специальные цены
            special_price = None
            if master.rating > 4.7:
                special_price = service.price * Decimal('1.2')  # +20% для топовых мастеров
            elif master.experience > 8:
                special_price = service.price * Decimal('1.1')  # +10% для опытных мастеров
            
            ms, created = MasterService.objects.get_or_create(
                master=master,
                service=service,
                defaults={
                    'is_available': True,
                    'special_price': special_price
                }
            )
            
            if created:
                master_services_created += 1
    
    print(f'Создано {master_services_created} связей мастер-услуга')

def create_test_data():
    """Основная функция для создания тестовых данных"""
    print("Начинаем создание тестовых данных...")
    
    # Очищаем базу (осторожно!)
    # Salon.objects.all().delete()
    # Service.objects.all().delete()
    # Master.objects.all().delete()
    # MasterService.objects.all().delete()
    
    # Создаем данные
    salons = create_salons()
    services = create_services()
    masters = create_masters(salons)
    assign_services_to_masters(masters, services)
    
    print("\nТестовые данные успешно созданы!")
    print(f"Создано:")
    print(f"- Салоны: {len(salons)}")
    print(f"- Услуги: {len(services)}")
    print(f"- Мастера: {len(masters)}")
    print(f"- Связей мастер-услуга: {MasterService.objects.count()}")

if __name__ == '__main__':
    create_test_data()