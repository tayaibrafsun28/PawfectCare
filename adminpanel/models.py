from django.db import models

# Employee model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Noon', 'Noon'),
        ('Evening', 'Evening'),
        ('Night', 'Night'),
    ]
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)

    SECTION_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
    ]
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)

    def __str__(self):
        return self.name

# Package model
class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

# Customer model (updated)
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    area = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)

    PET_TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
    ]
    pet_type = models.CharField(max_length=10, choices=PET_TYPE_CHOICES)
    breed = models.CharField(max_length=50, blank=True)
    vaccinated = models.CharField(max_length=10, blank=True)
    food_pref = models.CharField(max_length=100, blank=True)
    pet_notes = models.TextField(blank=True)

    date = models.DateField()
    time = models.TimeField()

    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    food_source = models.CharField(max_length=50, blank=True)
    booking_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.package.name}"
