from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from cars.models import Car, CarImage
from .models import Advertisement, Enquiry, DealerSettings

# File upload safety check helper
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']

def validate_image_file(file_obj):
    if not file_obj:
        return True, None
    ext = file_obj.name.lower()[file_obj.name.rfind('.'):]
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return False, f"Invalid image file extension '{ext}'. Allowed extensions: .jpg, .jpeg, .png, .webp"
    if file_obj.size > 10 * 1024 * 1024:  # 10 MB limit
        return False, "Image size exceeds maximum limit of 10MB."
    return True, None


def dealer_login(request):
    """
    Custom dealer login view processing username and password manually (No forms.py).
    """
    if request.user.is_authenticated:
        return redirect('dealer_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'dealer/login.html', {'old_username': username})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next') or 'dealer_dashboard'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'dealer/login.html', {'old_username': username})

    return render(request, 'dealer/login.html')


@login_required
def dealer_logout(request):
    """
    Logs out dealer user.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('dealer_login')


@login_required
def dealer_dashboard(request):
    """
    Dealer dashboard overview metrics.
    """
    total_cars = Car.objects.count()
    published_cars = Car.objects.filter(published=True).count()
    sold_cars = Car.objects.filter(sold=True).count()
    total_enquiries = Enquiry.objects.count()
    new_enquiries_count = Enquiry.objects.filter(status='New').count()
    active_ads_count = Advertisement.objects.filter(active=True).count()

    recent_cars = Car.objects.order_by('-created_at')[:5]
    recent_enquiries = Enquiry.objects.select_related('car').order_by('-created_at')[:5]

    context = {
        'active_tab': 'dashboard',
        'total_cars': total_cars,
        'published_cars': published_cars,
        'sold_cars': sold_cars,
        'total_enquiries': total_enquiries,
        'new_enquiries_count': new_enquiries_count,
        'active_ads_count': active_ads_count,
        'recent_cars': recent_cars,
        'recent_enquiries': recent_enquiries,
    }
    return render(request, 'dealer/dashboard.html', context)


# ==============================================================================
# DEALER CAR CRUD (NO FORMS.PY)
# ==============================================================================

@login_required
def dealer_car_list(request):
    """
    Dealer car inventory list view with search & pagination.
    """
    cars_list = Car.objects.all().order_by('-created_at')
    
    q = request.GET.get('q', '').strip()
    if q:
        cars_list = cars_list.filter(brand__icontains=q) | cars_list.filter(model__icontains=q)

    paginator = Paginator(cars_list, 10)
    page = request.GET.get('page')
    cars = paginator.get_page(page)

    context = {
        'active_tab': 'cars_list',
        'cars': cars,
        'q': q,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/cars/list.html', context)


def is_checked(request, key, default=True):
    """
    Robust checker for form controls (selects & checkboxes) across mobile and desktop.
    """
    val = request.POST.get(key)
    if val is None:
        return default
    return str(val).lower() in ['on', 'true', '1', 'yes', 'published']


@login_required
def dealer_car_create(request):
    """
    Add new car view parsing request.POST and request.FILES manually (No forms.py).
    """
    if request.method == 'POST':
        brand = request.POST.get('brand', '').strip()
        model = request.POST.get('model', '').strip()
        year = request.POST.get('year', '').strip()
        reg_year = request.POST.get('registration_year', '').strip()
        price = request.POST.get('price', '').strip()
        price_negotiable = is_checked(request, 'price_negotiable', default=True)
        km_driven = request.POST.get('km_driven', '').strip()
        fuel_type = request.POST.get('fuel_type', 'Petrol')
        transmission = request.POST.get('transmission', 'Manual')
        color = request.POST.get('color', '').strip()
        owners = request.POST.get('owners', '1').strip()
        insurance_valid = is_checked(request, 'insurance_valid', default=True)
        location = request.POST.get('location', 'Bhavnagar, Gujarat').strip()
        description = request.POST.get('description', '').strip()
        published = is_checked(request, 'published', default=True)
        sold = is_checked(request, 'sold', default=False)

        errors = []
        if not brand:
            errors.append('Brand is required.')
        if not model:
            errors.append('Model is required.')
        if not year or not year.isdigit():
            errors.append('Valid manufacturing year is required.')
        if not price:
            errors.append('Price is required.')
        if not km_driven or not km_driven.isdigit():
            errors.append('Valid KM driven is required.')

        main_image = request.FILES.get('main_image')
        valid_img, img_err = validate_image_file(main_image)
        if not valid_img:
            errors.append(img_err)

        if errors:
            for err in errors:
                messages.error(request, err)
            context = {
                'active_tab': 'cars_add',
                'old_data': request.POST,
                'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
            }
            return render(request, 'dealer/cars/create.html', context)

        # Create Car record
        car = Car.objects.create(
            brand=brand,
            model=model,
            year=int(year),
            registration_year=int(reg_year) if reg_year and reg_year.isdigit() else None,
            price=price,
            price_negotiable=price_negotiable,
            km_driven=int(km_driven),
            fuel_type=fuel_type,
            transmission=transmission,
            color=color,
            owners=int(owners) if owners and owners.isdigit() else 1,
            insurance_valid=insurance_valid,
            location=location,
            description=description,
            published=published,
            sold=sold,
            main_image=main_image if main_image else None
        )

        # Handle multiple additional images
        additional_images = request.FILES.getlist('images')
        for idx, img in enumerate(additional_images):
            valid, _ = validate_image_file(img)
            if valid:
                CarImage.objects.create(
                    car=car,
                    image=img,
                    display_order=idx + 1
                )

        messages.success(request, f'Car "{car.brand} {car.model}" created successfully!')
        return redirect('dealer_car_list')

    context = {
        'active_tab': 'cars_add',
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/cars/create.html', context)


@login_required
def dealer_car_detail(request, pk):
    """
    View car details inside dealer portal.
    """
    car = get_object_or_404(Car, pk=pk)
    context = {
        'active_tab': 'cars_list',
        'car': car,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/cars/detail.html', context)


@login_required
def dealer_car_edit(request, pk):
    """
    Edit existing car details & gallery images (No forms.py).
    """
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        # Check if deleting a specific gallery image
        delete_image_id = request.POST.get('delete_image_id')
        if delete_image_id:
            img_obj = CarImage.objects.filter(pk=delete_image_id, car=car).first()
            if img_obj:
                img_obj.delete()
                messages.success(request, 'Gallery image deleted.')
            return redirect('dealer_car_edit', pk=car.pk)

        # Update main car fields
        brand = request.POST.get('brand', '').strip()
        model = request.POST.get('model', '').strip()
        year = request.POST.get('year', '').strip()
        reg_year = request.POST.get('registration_year', '').strip()
        price = request.POST.get('price', '').strip()
        price_negotiable = is_checked(request, 'price_negotiable', default=False)
        km_driven = request.POST.get('km_driven', '').strip()
        fuel_type = request.POST.get('fuel_type', car.fuel_type)
        transmission = request.POST.get('transmission', car.transmission)
        color = request.POST.get('color', '').strip()
        owners = request.POST.get('owners', '1').strip()
        insurance_valid = is_checked(request, 'insurance_valid', default=False)
        location = request.POST.get('location', car.location).strip()
        description = request.POST.get('description', '').strip()
        published = is_checked(request, 'published', default=False)
        sold = is_checked(request, 'sold', default=False)

        errors = []
        if not brand:
            errors.append('Brand is required.')
        if not model:
            errors.append('Model is required.')
        if not year or not year.isdigit():
            errors.append('Valid year is required.')
        if not price:
            errors.append('Price is required.')

        main_image = request.FILES.get('main_image')
        if main_image:
            valid_img, img_err = validate_image_file(main_image)
            if not valid_img:
                errors.append(img_err)

        if errors:
            for err in errors:
                messages.error(request, err)
            context = {
                'active_tab': 'cars_list',
                'car': car,
                'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
            }
            return render(request, 'dealer/cars/edit.html', context)

        # Update Car model fields
        car.brand = brand
        car.model = model
        car.year = int(year)
        car.registration_year = int(reg_year) if reg_year and reg_year.isdigit() else None
        car.price = price
        car.price_negotiable = price_negotiable
        car.km_driven = int(km_driven) if km_driven and km_driven.isdigit() else car.km_driven
        car.fuel_type = fuel_type
        car.transmission = transmission
        car.color = color
        car.owners = int(owners) if owners and owners.isdigit() else car.owners
        car.insurance_valid = insurance_valid
        car.location = location
        car.description = description
        car.published = published
        car.sold = sold

        if main_image:
            car.main_image = main_image

        car.save()

        # Handle additional gallery uploads
        additional_images = request.FILES.getlist('images')
        for idx, img in enumerate(additional_images):
            valid, _ = validate_image_file(img)
            if valid:
                CarImage.objects.create(
                    car=car,
                    image=img,
                    display_order=car.images.count() + idx + 1
                )

        messages.success(request, f'Car "{car.brand} {car.model}" updated successfully!')
        return redirect('dealer_car_list')

    context = {
        'active_tab': 'cars_list',
        'car': car,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/cars/edit.html', context)


@login_required
def dealer_car_delete(request, pk):
    """
    Delete car confirmation & execution view. Uses POST for destructive delete.
    """
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        car_name = f"{car.brand} {car.model}"
        car.delete()
        messages.success(request, f'Car "{car_name}" deleted successfully.')
        return redirect('dealer_car_list')

    context = {
        'active_tab': 'cars_list',
        'car': car,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/cars/delete.html', context)


# ==============================================================================
# DEALER ADVERTISEMENT CRUD (NO FORMS.PY)
# ==============================================================================

@login_required
def dealer_ad_list(request):
    """
    List all banner advertisements.
    """
    ads = Advertisement.objects.all()
    context = {
        'active_tab': 'ads_list',
        'ads': ads,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/advertisements/list.html', context)


@login_required
def dealer_ad_create(request):
    """
    Create advertisement view (No forms.py).
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        button_text = request.POST.get('button_text', 'Learn More').strip()
        button_url = request.POST.get('button_url', '').strip()
        active = request.POST.get('active') == 'on'
        display_order = request.POST.get('display_order', '0').strip()
        image = request.FILES.get('image')

        errors = []
        if not title:
            errors.append('Title is required.')

        valid_img, img_err = validate_image_file(image)
        if not valid_img:
            errors.append(img_err)

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'dealer/advertisements/create.html', {'old_data': request.POST, 'active_tab': 'ads_add'})

        Advertisement.objects.create(
            title=title,
            subtitle=subtitle,
            button_text=button_text,
            button_url=button_url,
            active=active,
            display_order=int(display_order) if display_order.isdigit() else 0,
            image=image if image else None
        )

        messages.success(request, f'Advertisement "{title}" created successfully.')
        return redirect('dealer_ad_list')

    context = {
        'active_tab': 'ads_add',
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/advertisements/create.html', context)


@login_required
def dealer_ad_edit(request, pk):
    """
    Edit advertisement view (No forms.py).
    """
    ad = get_object_or_404(Advertisement, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        button_text = request.POST.get('button_text', 'Learn More').strip()
        button_url = request.POST.get('button_url', '').strip()
        active = request.POST.get('active') == 'on'
        display_order = request.POST.get('display_order', '0').strip()
        image = request.FILES.get('image')

        if not title:
            messages.error(request, 'Title is required.')
            return render(request, 'dealer/advertisements/edit.html', {'ad': ad, 'active_tab': 'ads_list'})

        if image:
            valid_img, img_err = validate_image_file(image)
            if not valid_img:
                messages.error(request, img_err)
                return render(request, 'dealer/advertisements/edit.html', {'ad': ad, 'active_tab': 'ads_list'})
            ad.image = image

        ad.title = title
        ad.subtitle = subtitle
        ad.button_text = button_text
        ad.button_url = button_url
        ad.active = active
        ad.display_order = int(display_order) if display_order.isdigit() else ad.display_order
        ad.save()

        messages.success(request, f'Advertisement "{ad.title}" updated successfully.')
        return redirect('dealer_ad_list')

    context = {
        'active_tab': 'ads_list',
        'ad': ad,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/advertisements/edit.html', context)


@login_required
def dealer_ad_delete(request, pk):
    """
    Delete advertisement confirmation & POST execution.
    """
    ad = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        title = ad.title
        ad.delete()
        messages.success(request, f'Advertisement "{title}" deleted successfully.')
        return redirect('dealer_ad_list')

    context = {
        'active_tab': 'ads_list',
        'ad': ad,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/advertisements/delete.html', context)


# ==============================================================================
# DEALER ENQUIRIES & SETTINGS
# ==============================================================================

@login_required
def dealer_enquiry_list(request):
    """
    Manage customer enquiries & update status.
    """
    enquiries_list = Enquiry.objects.select_related('car').all()
    
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        enquiries_list = enquiries_list.filter(status=status_filter)

    paginator = Paginator(enquiries_list, 15)
    page = request.GET.get('page')
    enquiries = paginator.get_page(page)

    context = {
        'active_tab': 'enquiries',
        'enquiries': enquiries,
        'selected_status': status_filter,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/enquiries/list.html', context)


@login_required
def dealer_enquiry_detail(request, pk):
    """
    View single enquiry and allow status update via POST.
    """
    enquiry = get_object_or_404(Enquiry, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status', enquiry.status)
        if new_status in ['New', 'Contacted', 'Closed']:
            enquiry.status = new_status
            enquiry.save()
            messages.success(request, f'Enquiry status updated to "{new_status}".')
            return redirect('dealer_enquiry_detail', pk=enquiry.pk)

    context = {
        'active_tab': 'enquiries',
        'enquiry': enquiry,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/enquiries/detail.html', context)


@login_required
def dealer_settings_edit(request):
    """
    Manage dealership settings, contact details, logo, dealer image (No forms.py).
    """
    settings_obj, created = DealerSettings.objects.get_or_create(id=1)

    if request.method == 'POST':
        dealership_name = request.POST.get('dealership_name', 'Sitaram Cars').strip()
        contact_name = request.POST.get('contact_name', 'YASH PARMAR').strip()
        phone = request.POST.get('phone', '6354895277').strip()
        whatsapp_number = request.POST.get('whatsapp_number', '916354895277').strip()
        about_text = request.POST.get('about_text', '').strip()

        logo = request.FILES.get('logo')
        dealer_image = request.FILES.get('dealer_image')

        if logo:
            valid, img_err = validate_image_file(logo)
            if valid:
                settings_obj.logo = logo

        if dealer_image:
            valid, img_err = validate_image_file(dealer_image)
            if valid:
                settings_obj.dealer_image = dealer_image

        settings_obj.dealership_name = dealership_name
        settings_obj.contact_name = contact_name
        settings_obj.phone = phone
        settings_obj.whatsapp_number = whatsapp_number
        settings_obj.about_text = about_text
        settings_obj.save()

        messages.success(request, 'Dealership settings updated successfully!')
        return redirect('dealer_settings_edit')

    context = {
        'active_tab': 'settings',
        'dealer_settings_obj': settings_obj,
        'new_enquiries_count': Enquiry.objects.filter(status='New').count(),
    }
    return render(request, 'dealer/settings/edit.html', context)
