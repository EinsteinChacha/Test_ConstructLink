from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class AccountType(models.TextChoices):
        EQUIPMENT_OWNER = 'equipment_owner', 'Equipment Owner'
        CONTRACTOR = 'contractor', 'Contractor'
        DRIVER = 'driver', 'Driver'
        LOGISTICS_PARTNER = 'logistics_partner', 'Logistics Partner'
        CONSTRUCTION_COMPANY = 'construction_company', 'Construction Company'
        INDIVIDUAL_CLIENT = 'individual_client', 'Individual Client'

    account_type = models.CharField(max_length=32, choices=AccountType.choices)

    def __str__(self):
        return f"{self.username} ({self.get_account_type_display()})"


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        UNAVAILABLE = 'unavailable', 'Unavailable'

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_listings')
    category = models.ForeignKey(EquipmentCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    description = models.TextField()
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    daily_price = models.DecimalField(max_digits=12, decimal_places=2)
    availability_status = models.CharField(
        max_length=20,
        choices=AvailabilityStatus.choices,
        default=AvailabilityStatus.AVAILABLE,
    )
    photo = models.ImageField(upload_to='equipment_photos/', blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.region}"


class BookingRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='booking_requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    start_date = models.DateField()
    end_date = models.DateField()
    site_location = models.CharField(max_length=255)
    purpose_of_use = models.TextField()
    contact_phone = models.CharField(max_length=30)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be before start date.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.equipment.name} booking by {self.requested_by.username}"
