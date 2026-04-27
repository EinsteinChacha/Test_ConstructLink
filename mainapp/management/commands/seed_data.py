from django.core.management.base import BaseCommand

from mainapp.models import Equipment, EquipmentCategory, User


class Command(BaseCommand):
    help = 'Seeds sample equipment categories and sample equipment'

    def handle(self, *args, **options):
        category_names = [
            'Excavator',
            'Wheel Loader',
            'Bulldozer',
            'Crane',
            'Tipper Truck',
            'Concrete Mixer',
            'Grader',
            'Roller',
            'Water Bowser',
        ]

        categories = {}
        for name in category_names:
            category, _ = EquipmentCategory.objects.get_or_create(name=name)
            categories[name] = category

        owner, _ = User.objects.get_or_create(
            username='sample_owner',
            defaults={'email': 'owner@example.com', 'account_type': User.AccountType.EQUIPMENT_OWNER},
        )
        if not owner.has_usable_password():
            owner.set_password('SamplePass123!')
            owner.save(update_fields=['password'])

        samples = [
            ('CAT 320 Excavator', 'Excavator', 'Dar es Salaam', 'Kinondoni', 'High-performance excavator for heavy digging.', 650000),
            ('Komatsu D65 Bulldozer', 'Bulldozer', 'Arusha', 'Arumeru', 'Reliable bulldozer for earthmoving jobs.', 580000),
            ('XCMG Truck Crane', 'Crane', 'Dodoma', 'Dodoma Urban', 'Mobile crane suitable for site lifting.', 900000),
        ]

        for name, cat, region, district, desc, daily_price in samples:
            Equipment.objects.get_or_create(
                owner=owner,
                name=name,
                defaults={
                    'category': categories[cat],
                    'description': desc,
                    'region': region,
                    'district': district,
                    'daily_price': daily_price,
                    'availability_status': Equipment.AvailabilityStatus.AVAILABLE,
                },
            )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
