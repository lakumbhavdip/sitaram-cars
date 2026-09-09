from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='advertisements/')
    button_text = models.CharField(max_length=50, default='Learn More', blank=True)
    button_url = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    car = models.ForeignKey('cars.Car', on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        car_info = f" for {self.car.brand} {self.car.model}" if self.car else ""
        return f"Enquiry from {self.name} ({self.phone}){car_info}"


class DealerSettings(models.Model):
    dealership_name = models.CharField(max_length=150, default='Sitaram Cars')
    contact_name = models.CharField(max_length=100, default='YASH PARMAR')
    phone = models.CharField(max_length=20, default='6354895277')
    whatsapp_number = models.CharField(max_length=20, default='6354895277')
    about_text = models.TextField(default='Welcome to Sitaram Cars. We provide quality certified used cars with transparent deals and trusted service.')
    logo = models.ImageField(upload_to='settings/', null=True, blank=True)
    dealer_image = models.ImageField(upload_to='settings/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dealership_name
