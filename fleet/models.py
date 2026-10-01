from django.conf import settings
from django.db import models

class Vehicle(models.Model):

    class VehicleType(models.TextChoices):
        TRUCK = "TRUCK", "Truck"
        VAN = "VAN", "Van"
        BUS = "BUS", "Bus"
        MINI_TRUCK = "MINI_TRUCK", "Mini Truck"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_TRANSIT = "IN_TRANSIT", "In Transit"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        INACTIVE = "INACTIVE", "Inactive"

    registration_number = models.CharField(max_length=20,unique=True)
    vehicle_type = models.CharField(max_length=20,choices=VehicleType.choices)
    model = models.CharField(max_length=100,blank=True)
    manufacturer = models.CharField(max_length=100,blank=True)
    manufacturing_year = models.PositiveIntegerField(null=True,blank=True)
    capacity = models.DecimalField(max_digits=10,decimal_places=2)
    fuel_type = models.CharField(max_length=30,blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.registration_number

class VehicleAssignment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="assignments")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null=True, related_name="vehicle_assignments_created")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.vehicle.registration_number} - "
            f"{self.status}"
        )


class VehicleMaintenance(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name="maintenance_records")

    maintenance_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    maintenance_date = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,related_name="maintenance_records_created")
    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.vehicle.registration_number} - "
            f"{self.maintenance_type}"
        )