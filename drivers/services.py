from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from fleet.models import VehicleAssignment
from fleet.services import assign_vehicle, complete_assignment
from .models import Driver, DriverAssignment

@transaction.atomic
def create_driver(validated_data, created_by):
    driver = Driver.objects.create(
        created_by=created_by,
        **validated_data
    )
    return driver

@transaction.atomic
def assign_driver_to_vehicle(
    driver,
    vehicle,
    assigned_by,
    start_time=None,
    notes=""
):
    if driver.status != Driver.Status.AVAILABLE:
        raise ValidationError(
            "Driver is not available for assignment."
        )
    if vehicle.status != vehicle.Status.AVAILABLE:
        raise ValidationError(
            "Vehicle is not available for assignment."
        )
    existing_driver_assignment = DriverAssignment.objects.filter(
        driver=driver,
        status=DriverAssignment.Status.ACTIVE
    ).first()

    if existing_driver_assignment:
        raise ValidationError(
            "Driver already has an active assignment."
        )

    if start_time is None:
        start_time = timezone.now()

    vehicle_assignment = assign_vehicle(
        vehicle=vehicle,
        assigned_by=assigned_by,
        start_time=start_time,
        notes=notes
    )
    driver_assignment = DriverAssignment.objects.create(
        driver=driver,
        vehicle_assignment=vehicle_assignment,
        assigned_by=assigned_by,
        start_time=start_time,
        notes=notes
    )

    driver.status = Driver.Status.ASSIGNED
    driver.save(update_fields=["status", "updated_at"])

    return driver_assignment

@transaction.atomic
def complete_driver_assignment(
    driver_assignment,
    end_time=None
):
    if driver_assignment.status != DriverAssignment.Status.ACTIVE:
        raise ValidationError(
            "Driver assignment is not active."
        )
    if end_time is None:
        end_time = timezone.now()

    if end_time <= driver_assignment.start_time:
        raise ValidationError(
            "End time must be after start time."
        )
    complete_assignment(
        driver_assignment.vehicle_assignment
    )
    driver_assignment.status = (
        DriverAssignment.Status.COMPLETED
    )
    driver_assignment.end_time = end_time
    driver_assignment.save(
        update_fields=[
            "status",
            "end_time",
            "updated_at"
        ]
    )

    driver = driver_assignment.driver
    driver.status = Driver.Status.AVAILABLE
    driver.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
    return driver_assignment

@transaction.atomic
def deactivate_driver(driver):

    active_assignment = DriverAssignment.objects.filter(
        driver=driver,
        status=DriverAssignment.Status.ACTIVE
    ).exists()

    if active_assignment:
        raise ValidationError(
            "Driver has an active assignment. "
            "Complete the assignment before deactivating."
        )
    driver.status = Driver.Status.INACTIVE
    driver.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )

    return driver