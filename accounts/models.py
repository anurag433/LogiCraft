from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        FLEET_MANAGER = "FLEET_MANAGER", "Fleet Manager"
        WAREHOUSE_MANAGER = "WAREHOUSE_MANAGER", "Warehouse Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    name = models.CharField()
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=20, blank=True)
    role = models.CharField(choices=Role.choices, default=Role.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username