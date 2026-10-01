from django.conf import settings
from django.db import models


class Driver(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        ASSIGNED = "ASSIGNED", "Assigned"
        ON_TRIP = "ON_TRIP", "On Trip"
        INACTIVE = "INACTIVE", "Inactive"

    driver_id = models.CharField(max_length=20,unique=True,editable=False)
    employee_id = models.CharField(max_length=30,unique=True)
    name = models.CharField( max_length=100)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(blank=True,null=True)

    license_number = models.CharField(max_length=50,unique=True)
    license_expiry_date = models.DateField(null=True,blank=True)

    experience_years = models.PositiveIntegerField(default=0)
    address = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drivers_created"
    )

    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.driver_id:
            last_driver = Driver.objects.order_by("-id").first()
            if last_driver:
                next_number = last_driver.id + 1
            else:
                next_number = 1
            self.driver_id = f"DRV{next_number:05d}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.employee_id} - {self.name}"


class DriverAssignment(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    driver = models.ForeignKey(Driver,on_delete=models.CASCADE,related_name="assignments")
    vehicle_assignment = models.OneToOneField(
        "fleet.VehicleAssignment",
        on_delete=models.CASCADE,
        related_name="driver_assignment"
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="driver_assignments_created"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True,blank=True)

    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["driver"],
                condition=models.Q(status="ACTIVE"),
                name="unique_active_driver_assignment"
            )
        ]
    def __str__(self):
        return (
            f"{self.driver.name} - "
            f"{self.vehicle_assignment.vehicle.registration_number}"
        )