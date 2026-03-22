from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Customer, Client

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
def clients(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    customer = Customer.objects.get(id=customer_id)
    client_list = Client.objects.filter(customer=customer)
    return render(request, 'core/clients.html', {'clients': client_list})

def add_client(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    if request.method == 'POST':
        from .models import Client
        Client.objects.create(
            customer_id=customer_id,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            notes=request.POST.get('notes'),
        )
        return redirect('clients')
    return render(request, 'core/add_client.html')