from django.contrib import admin

from .models import (
    Vehicle,
    VehicleAssignment,
    VehicleMaintenance,
)
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "registration_number",
        "vehicle_type",
        "capacity",
        "status",
        "created_at",
    ]

    list_filter = [
        "vehicle_type",
        "status",
        "fuel_type",
    ]

    search_fields = [
        "registration_number",
        "model",
        "manufacturer",
    ]

    ordering = [
        "-created_at"
    ]


@admin.register(VehicleAssignment)
class VehicleAssignmentAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "vehicle",
        "assigned_by",
        "start_time",
        "end_time",
        "status",
    ]

    list_filter = [
        "status",
    ]

    search_fields = [
        "vehicle__registration_number",
        "assigned_by__username",
    ]

    ordering = [
        "-created_at"
    ]


@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "vehicle",
        "maintenance_type",
        "cost",
        "maintenance_date",
        "next_due_date",
        "status",
    ]

    list_filter = [
        "status",
        "maintenance_type",
    ]

    search_fields = [
        "vehicle__registration_number",
        "maintenance_type",
    ]

    ordering = [
        "-maintenance_date"
    ]