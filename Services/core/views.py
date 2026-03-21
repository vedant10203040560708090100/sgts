from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Customer

def home(request):
    return render(request, 'core/home.html')

def login_view(request):
    if request.method == 'POST':
        key = request.POST.get('activation_key').strip()
        try:
            customer = Customer.objects.get(activation_key=key)
            if customer.is_active():
                request.session['customer_id'] = customer.id
                request.session['firm_name'] = customer.firm_name
                return redirect('dashboard')
            else:
                error = 'Your activation key has expired. Please contact us to renew.'
        except Customer.DoesNotExist:
            error = 'Invalid activation key.'
        return render(request, 'core/login.html', {'error': error})
    return render(request, 'core/login.html')

def dashboard(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    customer = Customer.objects.get(id=customer_id)
    return render(request, 'core/dashboard.html', {'customer': customer})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def contact(request):
    return render(request, 'core/contact.html')