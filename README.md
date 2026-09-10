# Sitaram Cars - Production Quality Car Dealership Website & Dealer Management Dashboard

A complete, production-grade automotive dealership platform and custom management dashboard built for **Sitaram Cars** (Contact Person: **YASH PARMAR**, Phone: **6354895277**, WhatsApp: **916354895277**).

Built using **Python 3.14+**, **Django 6.x**, **SQLite / PostgreSQL ORM**, **Bootstrap 5**, **Bootstrap Icons**, and **HTML/Jinja templates**.

---

## MANDATORY FORM ARCHITECTURE

> [!IMPORTANT]
> **STRICT ARCHITECTURAL DIRECTIVE:**
> - **NO `forms.py` exists anywhere in this project.**
> - Django `Form` and `ModelForm` classes are NOT used for any CRUD operations.
> - All forms (Login, Car Create/Edit/Delete, Advertisement CRUD, Enquiry, Settings) are authored directly in HTML/Jinja templates (`templates/...`).
> - The Django views process submissions manually using `request.POST` and `request.FILES` with server-side validation and direct ORM model methods.

---

## Features

### Public Website
- **Hero Section**: Premium automotive theme with call & contact CTAs.
- **Search & Multi-Filter**: Search by brand, model, price range (Min/Max), fuel type (Petrol, Diesel, CNG, Electric, Hybrid), transmission (Manual, Automatic, AMT, CVT, DCT), and model year.
- **Car Detail Page**: Dynamic image gallery carousel, full vehicle specifications (Price in ₹, Negotiable badge, KM driven, Fuel, Transmission, Ownership, Location, Insurance status), and embedded direct inquiry form.
- **Call Now & WhatsApp Integration**: Pre-formatted WhatsApp links automatically including car brand, model, year, and price.
- **Promotional Advertisements**: Dynamic homepage banner carousel managed via dealer portal.
- **Floating WhatsApp Button**: Accessible across all public pages.

### Custom Dealer Portal (`/dealer/login/`)
- **Custom Dealer Auth**: Does NOT use Django `/admin/`. Uses a sleek HTML login interface connected to Django `authenticate()` and `login()`.
- **Interactive CLI Command**: `python manage.py create_dealer` to setup dealer superuser accounts cleanly.
- **Dashboard Overview**: Key metrics (Total Cars, Published, Sold, Total/New Enquiries, Active Ads), recent inventory, and quick navigation.
- **Car Inventory CRUD**: Create, edit, publish, mark as sold, upload main image, manage multiple gallery images, and delete cars.
- **Advertisement CRUD**: Manage banner promotions with custom CTA text, links, and display ordering.
- **Enquiry Management**: View customer leads, filter by status (`New`, `Contacted`, `Closed`), and trigger one-click phone/WhatsApp callbacks.
- **Dealership Settings**: Manage dealership name, contact person name, phone numbers, about text, logo, and dealer photo.

---

## Project Structure

```
Sitaramcars/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── cars/
│   ├── models.py         # Car, CarImage
│   ├── views.py          # Public views (home, list, detail, search, contact)
│   ├── urls.py
│   └── tests.py
├── dealer/
│   ├── management/
│   │   └── commands/
│   │       └── create_dealer.py   # CLI dealer user creation
│   ├── models.py          # Advertisement, Enquiry, DealerSettings
│   ├── views.py           # Dealer Auth, Dashboard, Car CRUD, Ad CRUD, Enquiries, Settings
│   ├── urls.py
│   └── tests.py
├── templates/
│   ├── base.html
│   ├── 404.html
│   ├── 500.html
│   ├── public/
│   ├── dealer/
│   └── components/
├── static/
│   ├── css/style.css
│   └── js/main.js
├── media/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation & Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Clone repository & Create Virtual Environment
```bash
git clone <repository-url>
cd Sitaramcars
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Dealer Account
Run the custom interactive CLI command:
```bash
python manage.py create_dealer
```
Enter your desired dealer username and password when prompted.

### 6. Run Development Server
```bash
python manage.py runserver
```

Open your browser at:
- **Public Website**: `http://127.0.0.1:8000/`
- **Dealer Login Portal**: `http://127.0.0.1:8000/dealer/login/`

---

## Running Automated Test Suite

To run all 12 unit tests verifying public views, custom auth, search, filtering, and form-less CRUD operations:

```bash
python manage.py test
```

---

## Dealership Contact Details

- **Dealership Name**: Sitaram Cars
- **Contact Person**: YASH PARMAR
- **Contact Number**: 6354895277
- **WhatsApp**: 916354895277
