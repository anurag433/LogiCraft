from django.db import transaction
from django.utils import timezone
from .models import (Vehicle,VehicleAssignment,VehicleMaintenance,)

def create_vehicle(data):
    vehicle = Vehicle.objects.create(
        **data
    )
    return vehicle

def assign_vehicle(
    vehicle,
    assigned_by,
    start_time,
    end_time=None,
    notes=""
):
    if vehicle.status != Vehicle.Status.AVAILABLE:
        raise ValueError(
            "Vehicle is not available for assignment."
        )
    active_assignment = VehicleAssignment.objects.filter(
        vehicle=vehicle,
        status=VehicleAssignment.Status.ACTIVE
    ).exists()

    if active_assignment:
        raise ValueError(
            "Vehicle already has an active assignment."
        )

    assignment = VehicleAssignment.objects.create(
        vehicle=vehicle,
        assigned_by=assigned_by,
        start_time=start_time,
        end_time=end_time,
        notes=notes,
        status=VehicleAssignment.Status.ACTIVE
    )
    vehicle.status = Vehicle.Status.ASSIGNED
    vehicle.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
    return assignment

def complete_assignment(assignment):
    if assignment.status != VehicleAssignment.Status.ACTIVE:
        raise ValueError(
            "Assignment is not active."
        )
    assignment.status = (
        VehicleAssignment.Status.COMPLETED
    )
    assignment.end_time = (
        assignment.end_time
        or timezone.now()
    )
    assignment.save(
        update_fields=[
            "status",
            "end_time",
            "updated_at"
        ]
    )

    vehicle = assignment.vehicle
    vehicle.status = Vehicle.Status.AVAILABLE
    vehicle.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
    return assignment

def start_maintenance(
    vehicle,
    maintenance_data,
    created_by
):
    if vehicle.status == Vehicle.Status.IN_TRANSIT:
        raise ValueError(
            "Vehicle in transit cannot be sent "
            "for maintenance."
        )
    maintenance = VehicleMaintenance.objects.create(
        vehicle=vehicle,
        created_by=created_by,
        **maintenance_data
    )
    vehicle.status = Vehicle.Status.MAINTENANCE
    vehicle.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
    return maintenance

def complete_maintenance(maintenance):
    if maintenance.status == (
        VehicleMaintenance.Status.COMPLETED
    ):
        raise ValueError(
            "Maintenance is already completed."
        )
    maintenance.status = (
        VehicleMaintenance.Status.COMPLETED
    )
    maintenance.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )
    vehicle = maintenance.vehicle
    vehicle.status = Vehicle.Status.AVAILABLE
    vehicle.save(
        update_fields=["status", "updated_at"]
    )
    return maintenance