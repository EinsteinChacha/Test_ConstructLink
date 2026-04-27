from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import BookingRequest, Equipment, EquipmentCategory, User


class ConstructLinkModelTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner1',
            password='SecurePass123!',
            account_type=User.AccountType.EQUIPMENT_OWNER,
        )
        self.contractor = User.objects.create_user(
            username='contractor1',
            password='SecurePass123!',
            account_type=User.AccountType.CONTRACTOR,
        )
        self.category = EquipmentCategory.objects.create(name='Excavator')

    def test_equipment_creation(self):
        equipment = Equipment.objects.create(
            owner=self.owner,
            category=self.category,
            name='Test Excavator',
            description='Good equipment',
            region='Dar es Salaam',
            district='Ilala',
            daily_price=300000,
        )
        self.assertEqual(equipment.name, 'Test Excavator')
        self.assertEqual(equipment.owner, self.owner)

    def test_booking_request_creation(self):
        equipment = Equipment.objects.create(
            owner=self.owner,
            category=self.category,
            name='Booking Excavator',
            description='Ready for booking',
            region='Mwanza',
            district='Nyamagana',
            daily_price=400000,
        )
        booking = BookingRequest.objects.create(
            equipment=equipment,
            requested_by=self.contractor,
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 2),
            site_location='Mwanza City Site',
            purpose_of_use='Road grading',
            contact_phone='+255700111222',
        )
        self.assertEqual(booking.status, BookingRequest.Status.PENDING)

    def test_booking_end_date_validation(self):
        equipment = Equipment.objects.create(
            owner=self.owner,
            category=self.category,
            name='Validation Excavator',
            description='Validation',
            region='Mbeya',
            district='Mbeya Urban',
            daily_price=500000,
        )
        booking = BookingRequest(
            equipment=equipment,
            requested_by=self.contractor,
            start_date=date(2026, 6, 10),
            end_date=date(2026, 6, 9),
            site_location='Mbeya Site',
            purpose_of_use='Foundation prep',
            contact_phone='+255700333444',
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()


class DashboardRedirectTests(TestCase):
    def test_dashboard_redirect_for_contractor(self):
        user = User.objects.create_user(
            username='contractor_redirect',
            password='SecurePass123!',
            account_type=User.AccountType.CONTRACTOR,
        )
        self.client.login(username='contractor_redirect', password='SecurePass123!')
        response = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(response, reverse('contractor_dashboard'))
