from django.contrib import admin
from .models import Customer, Client

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['firm_name', 'contact_name', 'email', 'last_paid_at', 'key_expires_at', 'is_active']
    list_filter = ['key_expires_at']
    search_fields = ['firm_name', 'email']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'customer']
    search_fields = ['name', 'email']