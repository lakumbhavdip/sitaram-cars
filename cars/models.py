from django.db import models
from django.utils.text import slugify
import uuid

class Car(models.Model):
    FUEL_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Petrol + CNG', 'Petrol + CNG'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('Manual', 'Manual'),
        ('Automatic', 'Automatic'),
        ('AMT', 'AMT'),
        ('CVT', 'CVT'),
        ('DCT', 'DCT'),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    year = models.PositiveIntegerField()
    registration_year = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price amount in ₹")
    price_negotiable = models.BooleanField(default=True, verbose_name="Price Negotiable")
    km_driven = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Manual')
    color = models.CharField(max_length=50, blank=True)
    owners = models.PositiveIntegerField(default=1)
    insurance_valid = models.BooleanField(default=True, verbose_name="Insurance Valid")
    location = models.CharField(max_length=100, default='Bhavnagar, Gujarat')
    description = models.TextField(blank=True)
    published = models.BooleanField(default=True)
    sold = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='cars/main/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.model}-{self.year}")
            unique_slug = base_slug
            num = 1
            while Car.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - ₹{self.price}"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"Image for {self.car.brand} {self.car.model} #{self.id}"
