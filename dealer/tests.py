from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cars.models import Car
from dealer.models import Advertisement, Enquiry, DealerSettings

class DealerPortalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'yashdealer'
        self.password = 'Pass1234!'
        self.dealer_user = User.objects.create_superuser(
            username=self.username,
            email='yash@sitaramcars.com',
            password=self.password
        )
        self.dealer_settings = DealerSettings.objects.create(
            dealership_name='Sitaram Cars',
            contact_name='YASH PARMAR',
            phone='6354895277',
            whatsapp_number='916354895277'
        )

    def test_unauthenticated_dashboard_redirects_to_login(self):
        response = self.client.get(reverse('dealer_dashboard'))
        self.assertRedirects(response, f"/dealer/login/?next=/dealer/dashboard/")

    def test_custom_dealer_login_valid_credentials(self):
        post_data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(reverse('dealer_login'), post_data)
        self.assertRedirects(response, reverse('dealer_dashboard'))

    def test_custom_dealer_login_invalid_credentials(self):
        post_data = {
            'username': self.username,
            'password': 'WrongPassword'
        }
        response = self.client.post(reverse('dealer_login'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_dealer_car_crud_without_forms_py(self):
        self.client.login(username=self.username, password=self.password)

        # 1. CREATE CAR (POST)
        add_data = {
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2021,
            'price': 850000,
            'price_negotiable': 'on',
            'km_driven': 30000,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'color': 'Red',
            'owners': 1,
            'insurance_valid': 'on',
            'location': 'Surat, Gujarat',
            'description': 'Clean Civic car.',
            'published': 'on'
        }
        response_add = self.client.post(reverse('dealer_car_create'), add_data)
        self.assertRedirects(response_add, reverse('dealer_car_list'))

        car = Car.objects.filter(model='Civic').first()
        self.assertIsNotNone(car)
        self.assertEqual(car.brand, 'Honda')
        self.assertEqual(car.price, 850000)

        # 2. EDIT CAR (POST)
        edit_data = {
            'brand': 'Honda',
            'model': 'Civic RS',
            'year': 2021,
            'price': 820000,
            'price_negotiable': 'on',
            'km_driven': 31000,
            'fuel_type': 'Petrol',
            'transmission': 'Automatic',
            'color': 'Red',
            'owners': 1,
            'insurance_valid': 'on',
            'location': 'Surat, Gujarat',
            'description': 'Updated description.',
            'published': 'on'
        }
        response_edit = self.client.post(reverse('dealer_car_edit', kwargs={'pk': car.pk}), edit_data)
        self.assertRedirects(response_edit, reverse('dealer_car_list'))

        car.refresh_from_db()
        self.assertEqual(car.model, 'Civic RS')
        self.assertEqual(car.price, 820000)

        # 3. DELETE CAR (POST)
        response_delete = self.client.post(reverse('dealer_car_delete', kwargs={'pk': car.pk}))
        self.assertRedirects(response_delete, reverse('dealer_car_list'))
        self.assertFalse(Car.objects.filter(pk=car.pk).exists())

    def test_dealer_advertisement_crud_without_forms_py(self):
        self.client.login(username=self.username, password=self.password)

        ad_data = {
            'title': 'Mega Diwali Sale',
            'subtitle': 'Flat discounts on certified cars',
            'button_text': 'Check Deals',
            'button_url': '/cars/',
            'active': 'on',
            'display_order': 1
        }
        response_ad = self.client.post(reverse('dealer_ad_create'), ad_data)
        self.assertRedirects(response_ad, reverse('dealer_ad_list'))

        ad = Advertisement.objects.filter(title='Mega Diwali Sale').first()
        self.assertIsNotNone(ad)

        # Delete Ad
        response_del = self.client.post(reverse('dealer_ad_delete', kwargs={'pk': ad.pk}))
        self.assertRedirects(response_del, reverse('dealer_ad_list'))
        self.assertFalse(Advertisement.objects.filter(pk=ad.pk).exists())

    def test_dealer_enquiry_status_update(self):
        self.client.login(username=self.username, password=self.password)
        enquiry = Enquiry.objects.create(
            name='Customer A',
            phone='8888888888',
            message='Test message',
            status='New'
        )

        response = self.client.post(reverse('dealer_enquiry_detail', kwargs={'pk': enquiry.pk}), {'status': 'Contacted'})
        self.assertRedirects(response, reverse('dealer_enquiry_detail', kwargs={'pk': enquiry.pk}))
        
        enquiry.refresh_from_db()
        self.assertEqual(enquiry.status, 'Contacted')
