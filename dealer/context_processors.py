from .models import DealerSettings

def dealer_context(request):
    """
    Injects global dealership settings into all template contexts.
    If no record exists, returns a default fallback dictionary.
    """
    settings_obj = DealerSettings.objects.first()
    if settings_obj:
        return {'dealer_settings': settings_obj}
    
    return {
        'dealer_settings': {
            'dealership_name': 'Sitaram Cars',
            'contact_name': 'YASH PARMAR',
            'phone': '6354895277',
            'whatsapp_number': '916354895277',
            'about_text': 'Welcome to Sitaram Cars. We provide quality certified used cars with transparent deals and trusted service.',
        }
    }
