from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    # Packages
    path('packages/', views.packages, name='admin_packages'),
    path('packages/<int:id>/', views.packages, name='edit_package'),
    path('packages/delete/<int:id>/', views.delete_package, name='delete_package'),

    # Employees
    path('employees/', views.employees, name='admin_employees'),
    path('employees/<int:id>/', views.employees, name='edit_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    # Customers
    path('customers/', views.customers, name='admin_customers'),
    path('customers/<int:id>/', views.edit_customer, name='edit_customer'),
    path('customers/delete/<int:id>/', views.delete_customer, name='delete_customer'),

    # Messages
    path('messages/', views.messages_view, name='admin_messages'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/view/<int:message_id>/', views.view_message, name='view_message'),
]
