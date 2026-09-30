from rest_framework import serializers
from .models import (Vehicle, VehicleAssignment, VehicleMaintenance,)

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [ "id", "registration_number", "vehicle_type", "model", "manufacturer", "manufacturing_year", "capacity", "fuel_type", "status", "created_at","updated_at"]
        read_only_fields = ["id", "status", "created_at","updated_at"]

    def validate_registration_number(self, value):
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError(
                "Registration number is required."
            )
        return value

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Capacity must be greater than zero."
            )
        return value

    def validate_manufacturing_year(self, value):
        if value is not None and value < 1900:
            raise serializers.ValidationError(
                "Enter a valid manufacturing year."
            )
        return value

class VehicleMaintenanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = VehicleMaintenance
        fields = [
            "id",
            "vehicle",
            "maintenance_type",
            "description",
            "cost",
            "maintenance_date",
            "next_due_date",
            "status",
            "created_by",
            "created_at",
            "updated_at",
   
        ]
        read_only_fields = [
            "id",
            "created_by",
            "updated_at",
            
        ]

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Cost cannot be negative."
            )
        return value

class VehicleAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleAssignment
        fields = [
            "id",
            "vehicle",
            "assigned_by",
            "start_time",
            "end_time",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "assigned_by",
            "status",
            "created_at",
            "updated_at",
        ]
    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if end_time and end_time <= start_time:
            raise serializers.ValidationError({
                "end_time": (
                    "End time must be after start time."
                )
            })
        return attrs