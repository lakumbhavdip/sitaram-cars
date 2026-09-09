from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car
from dealer.models import Advertisement, Enquiry

def public_home(request):
    """
    Homepage view for Sitaram Cars.
    Displays hero section, search form, published cars, active advertisements,
    why choose us cards, and dealer contact CTA.
    """
    recent_cars = Car.objects.filter(published=True).order_by('-created_at')[:6]
    active_ads = Advertisement.objects.filter(active=True).order_by('display_order', '-created_at')
    
    # Extract distinct brands & models for search dropdowns
    brands = Car.objects.filter(published=True).values_list('brand', flat=True).distinct()
    
    context = {
        'recent_cars': recent_cars,
        'active_ads': active_ads,
        'brands': sorted(list(set(brands))),
    }
    return render(request, 'public/home.html', context)


def public_cars(request):
    """
    Public car listing page with search, multi-field filtering, sorting, and pagination.
    """
    cars_list = Car.objects.filter(published=True)

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        cars_list = cars_list.filter(
            Q(brand__icontains=q) |
            Q(model__icontains=q) |
            Q(description__icontains=q) |
            Q(color__icontains=q)
        )

    # Filters
    brand = request.GET.get('brand', '').strip()
    if brand:
        cars_list = cars_list.filter(brand__iexact=brand)

    model = request.GET.get('model', '').strip()
    if model:
        cars_list = cars_list.filter(model__icontains=model)

    fuel_type = request.GET.get('fuel_type', '').strip()
    if fuel_type:
        cars_list = cars_list.filter(fuel_type=fuel_type)

    transmission = request.GET.get('transmission', '').strip()
    if transmission:
        cars_list = cars_list.filter(transmission=transmission)

    min_price = request.GET.get('min_price', '').strip()
    if min_price and min_price.isdigit():
        cars_list = cars_list.filter(price__gte=int(min_price))

    max_price = request.GET.get('max_price', '').strip()
    if max_price and max_price.isdigit():
        cars_list = cars_list.filter(price__lte=int(max_price))

    year = request.GET.get('year', '').strip()
    if year and year.isdigit():
        cars_list = cars_list.filter(year=int(year))

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        cars_list = cars_list.order_by('price')
    elif sort_by == 'price_high':
        cars_list = cars_list.order_by('-price')
    elif sort_by == 'year_new':
        cars_list = cars_list.order_by('-year')
    else:
        cars_list = cars_list.order_by('-created_at')

    # Pagination
    paginator = Paginator(cars_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context choices for filter dropdowns
    brands = Car.objects.filter(published=True).values_list('brand', flat=True).distinct()

    context = {
        'page_obj': page_obj,
        'brands': sorted(list(set(brands))),
        'selected_brand': brand,
        'selected_model': model,
        'selected_fuel': fuel_type,
        'selected_transmission': transmission,
        'selected_sort': sort_by,
        'min_price': min_price,
        'max_price': max_price,
        'q': q,
    }
    return render(request, 'public/cars.html', context)


def public_car_detail(request, slug):
    """
    Detailed view of a specific car. Handles inquiry POST submission directly without forms.py.
    """
    car = get_object_or_404(Car, slug=slug)

    # Process embedded inquiry form directly from request.POST
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Name is required.')
        if not phone:
            errors.append('Phone number is required.')
        if not message:
            errors.append('Message is required.')

        if errors:
            for err in errors:
                messages.error(request, err)
        else:
            Enquiry.objects.create(
                name=name,
                phone=phone,
                email=email,
                car=car,
                message=message,
                status='New'
            )
            messages.success(request, 'Thank you! Your enquiry has been submitted successfully. Yash Parmar from Sitaram Cars will contact you shortly.')
            return redirect('public_car_detail', slug=slug)

    # Similar cars for recommendation
    similar_cars = Car.objects.filter(published=True, brand=car.brand).exclude(pk=car.pk)[:3]

    context = {
        'car': car,
        'gallery_images': car.images.all(),
        'similar_cars': similar_cars,
    }
    return render(request, 'public/car_detail.html', context)


def public_about(request):
    """
    About page for Sitaram Cars and Yash Parmar.
    """
    return render(request, 'public/about.html')


def public_contact(request):
    """
    Contact Us page with manual POST handling (No forms.py).
    """
    all_cars = Car.objects.filter(published=True, sold=False)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        car_id = request.POST.get('car', '').strip()
        message = request.POST.get('message', '').strip()

        errors = []
        if not name:
            errors.append('Please provide your name.')
        if not phone:
            errors.append('Please provide your phone number.')
        if not message:
            errors.append('Please enter your message or inquiry.')

        if errors:
            for err in errors:
                messages.error(request, err)
            context = {
                'cars': all_cars,
                'old_data': request.POST,
            }
            return render(request, 'public/contact.html', context)

        selected_car = None
        if car_id and car_id.isdigit():
            selected_car = Car.objects.filter(pk=int(car_id)).first()

        Enquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            car=selected_car,
            message=message,
            status='New'
        )

        messages.success(request, 'Your enquiry has been received! YASH PARMAR will contact you soon.')
        return redirect('public_contact')

    context = {
        'cars': all_cars,
    }
    return render(request, 'public/contact.html', context)
