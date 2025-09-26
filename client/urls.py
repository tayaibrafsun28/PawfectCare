from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.landing_page, name='home'),
    path('services/', views.services_page, name='services'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
    path('book/', views.book_page, name='book'),  # Booking page
    path('billing/<int:customer_id>/', views.billing_page, name='billing'),
    path('reviews/', views.reviews_page, name='reviews'),

    # Authentication
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_page, name='signup'),
]
