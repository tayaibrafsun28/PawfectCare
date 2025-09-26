from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from adminpanel.models import Employee, Package, Customer
from client.models import Message

# -----------------------------
# Admin user check
# -----------------------------
def is_admin_user(user):
    return user.is_authenticated and user.is_staff

# -----------------------------
# Dashboard view
# -----------------------------
@user_passes_test(is_admin_user, login_url='/login/')
def dashboard(request):
    context = {
        'employees_count': Employee.objects.count(),
        'packages_count': Package.objects.count(),
        'customers_count': Customer.objects.count(),
        'messages_count': Message.objects.count(),
    }
    return render(request, 'adminpanel/dashboard.html', context)

# -----------------------------
# Customers view
# -----------------------------
@user_passes_test(is_admin_user, login_url='/login/')
def customers(request):
    all_customers = Customer.objects.all()
    return render(request, 'adminpanel/customers.html', {'customers': all_customers})

# Add/Edit customer
@user_passes_test(is_admin_user, login_url='/login/')
def edit_customer(request, id=None):
    customer_to_edit = get_object_or_404(Customer, id=id) if id else None

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pet_type = request.POST.get('pet_type')
        date = request.POST.get('date')
        time = request.POST.get('time')
        package_id = request.POST.get('package')
        package = get_object_or_404(Package, id=package_id)

        if customer_to_edit:
            customer_to_edit.name = name
            customer_to_edit.phone = phone
            customer_to_edit.pet_type = pet_type
            customer_to_edit.date = date
            customer_to_edit.time = time
            customer_to_edit.package = package
            customer_to_edit.save()
        else:
            Customer.objects.create(
                name=name,
                phone=phone,
                pet_type=pet_type,
                date=date,
                time=time,
                package=package
            )

        return redirect('admin_customers')

    packages = Package.objects.all()
    return render(request, 'adminpanel/edit_customer.html', {
        'customer_to_edit': customer_to_edit,
        'packages': packages
    })

# Delete customer
@user_passes_test(is_admin_user, login_url='/login/')
def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect('admin_customers')

# -----------------------------
# Employees view
# -----------------------------
@user_passes_test(is_admin_user, login_url='/login/')
def employees(request, id=None):
    employee_to_edit = get_object_or_404(Employee, id=id) if id else None

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        salary = request.POST.get('salary')
        shift = request.POST.get('shift')
        section = request.POST.get('section')

        if employee_to_edit:
            employee_to_edit.name = name
            employee_to_edit.email = email
            employee_to_edit.phone = phone
            employee_to_edit.salary = salary
            employee_to_edit.shift = shift
            employee_to_edit.section = section
            employee_to_edit.save()
        else:
            if name and email and phone and salary and shift and section:
                Employee.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    salary=salary,
                    shift=shift,
                    section=section
                )
        return redirect('admin_employees')

    all_employees = Employee.objects.all()
    return render(request, 'adminpanel/employees.html', {
        'employees': all_employees,
        'employee_to_edit': employee_to_edit
    })

# Delete employee
@user_passes_test(is_admin_user, login_url='/login/')
def delete_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    employee.delete()
    return redirect('admin_employees')

# -----------------------------
# Messages view
# -----------------------------
@user_passes_test(is_admin_user, login_url='/login/')
def messages_view(request):
    messages_list = Message.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/messages.html', {'messages_list': messages_list})

# Delete message
@user_passes_test(is_admin_user, login_url='/login/')
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    msg.delete()
    return redirect('admin_messages')

# View single message (optional)
@user_passes_test(is_admin_user, login_url='/login/')
def view_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    return render(request, 'adminpanel/message_modal.html', {'msg': msg})

# -----------------------------
# Packages view
# -----------------------------
@user_passes_test(is_admin_user, login_url='/login/')
def packages(request, id=None):
    package_to_edit = get_object_or_404(Package, id=id) if id else None

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if package_to_edit:
            package_to_edit.name = name
            package_to_edit.price = price
            package_to_edit.description = description
            package_to_edit.save()
        else:
            if name and price and description:
                Package.objects.create(name=name, price=price, description=description)

        return redirect('admin_packages')

    all_packages = Package.objects.all()
    return render(request, 'adminpanel/packages.html', {
        'packages': all_packages,
        'package': package_to_edit
    })

# Delete package
@user_passes_test(is_admin_user, login_url='/login/')
def delete_package(request, id):
    package = get_object_or_404(Package, id=id)
    package.delete()
    return redirect('admin_packages')
