from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_client'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoices/add/', views.add_invoice, name='add_invoice'),
    path('invoices/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    ]
