from django.test import TestCase, Client
from django.urls import reverse
from cars.models import Car
from dealer.models import Enquiry, DealerSettings

class PublicViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.dealer_settings = DealerSettings.objects.create(
            dealership_name='Sitaram Cars',
            contact_name='YASH PARMAR',
            phone='6354895277',
            whatsapp_number='916354895277'
        )
        self.car = Car.objects.create(
            brand='Maruti Suzuki',
            model='Swift VXI',
            year=2022,
            price=600000,
            price_negotiable=True,
            km_driven=20000,
            fuel_type='Petrol',
            transmission='Manual',
            published=True
        )

    def test_homepage_status_code_200(self):
        response = self.client.get(reverse('public_home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sitaram Cars')
        self.assertContains(response, 'Find Your Perfect Car')

    def test_car_listing_page(self):
        response = self.client.get(reverse('public_cars'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maruti Suzuki')
        self.assertContains(response, 'Swift VXI')

    def test_car_listing_filtering(self):
        response = self.client.get(reverse('public_cars') + '?brand=Maruti+Suzuki&fuel_type=Petrol')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Swift VXI')

        # Filter non-existent brand
        response_empty = self.client.get(reverse('public_cars') + '?brand=Toyota')
        self.assertContains(response_empty, 'No cars available right now matching your criteria')

    def test_car_detail_page(self):
        response = self.client.get(reverse('public_car_detail', kwargs={'slug': self.car.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Swift VXI')
        self.assertContains(response, '6354895277')

    def test_car_detail_inquiry_post_without_forms_py(self):
        post_data = {
            'name': 'Ramesh Kumar',
            'phone': '9876543210',
            'email': 'ramesh@example.com',
            'message': 'Interested in buying this Maruti Swift.'
        }
        response = self.client.post(reverse('public_car_detail', kwargs={'slug': self.car.slug}), post_data)
        self.assertRedirects(response, reverse('public_car_detail', kwargs={'slug': self.car.slug}))
        
        # Verify Enquiry model saved directly from POST data
        enquiry = Enquiry.objects.filter(phone='9876543210').first()
        self.assertIsNotNone(enquiry)
        self.assertEqual(enquiry.name, 'Ramesh Kumar')
        self.assertEqual(enquiry.car, self.car)

    def test_contact_page_post_without_forms_py(self):
        post_data = {
            'name': 'Priya Patel',
            'phone': '9123456789',
            'email': 'priya@example.com',
            'message': 'Looking for a automatic SUV.'
        }
        response = self.client.post(reverse('public_contact'), post_data)
        self.assertRedirects(response, reverse('public_contact'))
        
        enquiry = Enquiry.objects.filter(phone='9123456789').first()
        self.assertIsNotNone(enquiry)
        self.assertEqual(enquiry.name, 'Priya Patel')
