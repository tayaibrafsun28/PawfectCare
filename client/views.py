# client/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from adminpanel.models import Package, Customer
from .models import Message, Review

# -----------------------------
# Home page
# -----------------------------
def landing_page(request):
    packages = Package.objects.order_by('-id')[:4]
    reviews = Review.objects.order_by('-created_at')[:3]
    return render(request, 'client/home.html', {'packages': packages, 'reviews': reviews})

# -----------------------------
# Services page
# -----------------------------
def services_page(request):
    packages = Package.objects.order_by('-id')
    return render(request, 'client/services.html', {'packages': packages})

# -----------------------------
# About page
# -----------------------------
def about_page(request):
    return render(request, 'client/about.html')

# -----------------------------
# Contact page (saves Message)
# -----------------------------
def contact_page(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        city = request.POST.get("city", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not message_text:
            messages.error(request, "Please fill in required fields.")
            return render(request, 'client/contact.html')

        Message.objects.create(
            name=name,
            email=email,
            phone=phone,
            city=city,
            message=message_text
        )

        messages.success(request, "Message sent successfully!")
        return redirect("contact")

    return render(request, 'client/contact.html')

# -----------------------------
# Login page
# -----------------------------
def login_page(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard') if request.user.is_staff else redirect('home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard') if user.is_staff else redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'client/login.html')

# -----------------------------
# Logout view
# -----------------------------
def logout_view(request):
    logout(request)
    return redirect('home')

# -----------------------------
# Signup page
# -----------------------------
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')

    return render(request, 'client/signup.html')

# -----------------------------
# Book page
# -----------------------------
def book_page(request):
    packages = Package.objects.all()

    if request.method == "POST":
        data = {
            'name': request.POST.get("name", "").strip(),
            'email': request.POST.get("email", "").strip(),
            'phone': request.POST.get("phone", "").strip(),
            'area': request.POST.get("area", "").strip(),
            'address': request.POST.get("address", "").strip(),
            'pet_type': request.POST.get("pet_type", "").strip(),
            'breed': request.POST.get("breed", "").strip(),
            'vaccinated': request.POST.get("vaccinated", "").strip(),
            'food_pref': request.POST.get("food_pref", "").strip(),
            'pet_notes': request.POST.get("pet_notes", "").strip(),
            'date': request.POST.get("date", "").strip(),
            'time': request.POST.get("time", "").strip(),
            'food_source': request.POST.get("food_source", "").strip(),
            'booking_notes': request.POST.get("booking_notes", "").strip()
        }

        package_id = request.POST.get("package")
        if not package_id:
            messages.error(request, "Please select a package.")
            return render(request, "client/book.html", {"packages": packages})

        required_fields = ['name', 'phone', 'address', 'pet_type', 'breed', 'food_pref', 'date', 'time']
        if not all(data[field] for field in required_fields):
            messages.error(request, "Please fill all required fields.")
            return render(request, "client/book.html", {"packages": packages})

        package = get_object_or_404(Package, id=package_id)

        customer = Customer.objects.create(package=package, **data)

        return redirect("billing", customer_id=customer.id)

    return render(request, "client/book.html", {"packages": packages})

# -----------------------------
# Billing page
# -----------------------------
def billing_page(request, customer_id=None):
    if customer_id:
        booking = get_object_or_404(Customer, id=customer_id)
    else:
        booking = Customer.objects.latest("id")
    return render(request, "client/billing.html", {"booking": booking})

# -----------------------------
# Reviews page
# -----------------------------
def reviews_page(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        reviewText = request.POST.get("reviewText", "").strip()
        rating = request.POST.get("rating", "").strip()

        if not name or not reviewText or not rating:
            messages.error(request, "Please fill all fields and select a rating.")
        else:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
                Review.objects.create(name=name, reviewText=reviewText, rating=rating)
                messages.success(request, "Thank you for your review!")
                return redirect("reviews")
            except ValueError:
                messages.error(request, "Invalid rating value.")

    reviews = Review.objects.order_by('-created_at')
    return render(request, 'client/reviews.html', {'reviews': reviews})
