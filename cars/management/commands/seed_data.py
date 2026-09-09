from django.core.management.base import BaseCommand
from cars.models import Car
from dealer.models import DealerSettings, Advertisement

class Command(BaseCommand):
    help = 'Seeds initial default dealer settings, sample cars, and banner ads for testing Sitaram Cars.'

    def handle(self, *args, **options):
        # 1. Seed DealerSettings
        settings_obj, created = DealerSettings.objects.get_or_create(id=1)
        settings_obj.dealership_name = 'Sitaram Cars'
        settings_obj.contact_name = 'YASH PARMAR'
        settings_obj.phone = '6354895277'
        settings_obj.whatsapp_number = '916354895277'
        settings_obj.about_text = 'Welcome to Sitaram Cars. Founded by Yash Parmar, we offer top quality certified pre-owned vehicles with complete transparent pricing, certified inspection, and customer-first service in Gujarat.'
        settings_obj.save()
        self.stdout.write(self.style.SUCCESS('Seeded DealerSettings for Sitaram Cars.'))

        # 2. Seed Sample Advertisements
        if not Advertisement.objects.exists():
            Advertisement.objects.create(
                title='Festive Season Car Sale at Sitaram Cars!',
                subtitle='Get the best pre-owned cars at unbeatable prices with easy financing and instant paperwork.',
                button_text='Explore Inventory',
                button_url='/cars/',
                active=True,
                display_order=1
            )
            Advertisement.objects.create(
                title='Want to Sell Your Car Fast?',
                subtitle='Get instant valuation and best cash offer directly from Yash Parmar.',
                button_text='Contact Dealer',
                button_url='/contact/',
                active=True,
                display_order=2
            )
            self.stdout.write(self.style.SUCCESS('Seeded sample Advertisements.'))

        # 3. Seed Sample Cars
        sample_cars = [
            {
                'brand': 'Maruti Suzuki',
                'model': 'Swift VXI',
                'year': 2022,
                'registration_year': 2022,
                'price': 625000,
                'price_negotiable': True,
                'km_driven': 24000,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'color': 'Pearl White',
                'owners': 1,
                'insurance_valid': True,
                'location': 'Surat, Gujarat',
                'description': 'Mint condition Maruti Swift VXI. Single owner driven, regularly serviced at authorized service center. Includes Bluetooth audio, power windows, ABS, and clean interior.',
                'published': True,
                'sold': False
            },
            {
                'brand': 'Hyundai',
                'model': 'Creta SX (O)',
                'year': 2021,
                'registration_year': 2021,
                'price': 1380000,
                'price_negotiable': True,
                'km_driven': 38000,
                'fuel_type': 'Diesel',
                'transmission': 'Automatic',
                'color': 'Phantom Black',
                'owners': 1,
                'insurance_valid': True,
                'location': 'Surat, Gujarat',
                'description': 'Top model Hyundai Creta SX Automatic Diesel. Panoramic sunroof, ventilated seats, Bose audio, leatherette upholstery. Complete service history available.',
                'published': True,
                'sold': False
            },
            {
                'brand': 'Honda',
                'model': 'City ZX',
                'year': 2020,
                'registration_year': 2020,
                'price': 990000,
                'price_negotiable': True,
                'km_driven': 42000,
                'fuel_type': 'Petrol',
                'transmission': 'CVT',
                'color': 'Golden Brown',
                'owners': 1,
                'insurance_valid': True,
                'location': 'Surat, Gujarat',
                'description': 'Ultra smooth Honda City ZX i-VTEC Automatic. Sunroof, LED headlights, alloy wheels, touch screen navigation, and new tires.',
                'published': True,
                'sold': False
            },
            {
                'brand': 'Tata',
                'model': 'Nexon XZ Plus',
                'year': 2023,
                'registration_year': 2023,
                'price': 1050000,
                'price_negotiable': False,
                'km_driven': 15000,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'color': 'Daytona Grey',
                'owners': 1,
                'insurance_valid': True,
                'location': 'Surat, Gujarat',
                'description': '5-Star GNCAP safety rated Tata Nexon. Like-new vehicle under company warranty. Digital cluster, Harman audio, rear AC vents.',
                'published': True,
                'sold': False
            },
            {
                'brand': 'Mahindra',
                'model': 'Thar LX Hard Top 4WD',
                'year': 2022,
                'registration_year': 2022,
                'price': 1420000,
                'price_negotiable': True,
                'km_driven': 21000,
                'fuel_type': 'Diesel',
                'transmission': 'Manual',
                'color': 'Napoli Black',
                'owners': 1,
                'insurance_valid': True,
                'location': 'Surat, Gujarat',
                'description': 'Iconic 4x4 Mahindra Thar LX Diesel Hardtop. Equipped with alloy wheels, touchscreen infotainment, and off-road capability.',
                'published': True,
                'sold': False
            }
        ]

        for car_data in sample_cars:
            if not Car.objects.filter(brand=car_data['brand'], model=car_data['model'], year=car_data['year']).exists():
                Car.objects.create(**car_data)
                self.stdout.write(self.style.SUCCESS(f"Seeded Car: {car_data['brand']} {car_data['model']}"))

        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
