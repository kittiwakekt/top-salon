import datetime
from django.test import TestCase
from django.db import DataError
from django.core.exceptions import ValidationError

from salon.models import Master, MasterService, Salon, Service

class SalonModelTest(TestCase):
    def test_create_salon(self):
        Salon.objects.create(
            name = 'f' * 50,
            address = 'rty' * 50,
            phone = '72224445896',
            opening_time = datetime.time(11, 30),
            closing_time = datetime.time(21, 30),
        )

        res = Salon.objects.filter(name='f' * 50)
        self.assertTrue(res.exists())

        self.assertEqual(res[0].address, 'rty' * 50)
        self.assertTrue(res[0].is_active)
        self.assertEqual(str(res[0]), 'f' * 50)

    def test_max_length(self):
        salon = Salon.objects.create(
            name = 'f' * 201,
            address = 'rty' * 201,
            phone = '72224445896' * 2,
            opening_time = datetime.time(11, 30),
            closing_time = datetime.time(21, 30),
        )
        res = Salon.objects.all()
        self.assertEqual(len(res), 1)

class MasterServiceModelTest(TestCase):
    def setUp(self):
        self.salon = Salon.objects.create(
            name = 'f' * 50,
            address = 'rty' * 50,
            phone = '72224445896',
            opening_time = datetime.time(11, 30),
            closing_time = datetime.time(21, 30),
        )
        self.master = Master.objects.create(
            salon = self.salon,
            first_name = 'd' * 20,
            last_name = 'f' * 15,
            specialization = 'hair',
            experience = 2,
            hire_date = datetime.date(2025, 10, 12),
        )
        self.service = Service.objects.create(
            name = 'f' * 50,
            category = 'face',
            duration = 30,
            price = 480.50,
        )

    def test_create(self):
        MasterService.objects.create(
            master = self.master,
            service = self.service
        )
        res = MasterService.objects.filter(master_id=self.master.id)
        self.assertEqual(len(res), 1)
