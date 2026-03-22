from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Customer, Client, Invoice, InvoiceItem

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

def invoices(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    invoice_list = Invoice.objects.filter(customer_id=customer_id).order_by('-created_at')
    return render(request, 'core/invoices.html', {'invoices': invoice_list})

def add_invoice(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    customer = Customer.objects.get(id=customer_id)
    clients = Client.objects.filter(customer=customer)
    if request.method == 'POST':
        invoice = Invoice.objects.create(
            customer_id=customer_id,
            client_id=request.POST.get('client') or None,
            invoice_number=request.POST.get('invoice_number'),
            due_date=request.POST.get('due_date'),
            notes=request.POST.get('notes'),
            status='draft',
            total=0
        )
        descriptions = request.POST.getlist('description')
        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('unit_price')
        print("descriptions:", descriptions)
        print("quantities:", quantities)
        print("prices:", prices)
        total = 0
        for i in range(len(descriptions)):
            if descriptions[i] and quantities[i] and prices[i]:
                try:
                    qty = float(quantities[i])
                    price = float(prices[i])
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=descriptions[i],
                        quantity=qty,
                        unit_price=price
                    )
                    total += qty * price
                except ValueError:
                    pass
        invoice.total = total
        invoice.save()
        return redirect('invoices')
    return render(request, 'core/add_invoice.html', {'clients': clients})

def view_invoice(request, invoice_id):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('login')
    invoice = Invoice.objects.get(id=invoice_id, customer_id=customer_id)
    return render(request, 'core/view_invoice.html', {'invoice': invoice})