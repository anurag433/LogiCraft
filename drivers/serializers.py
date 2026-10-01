from django.utils import timezone
from rest_framework import serializers
from .models import Driver, DriverAssignment

class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = [
            "id",
            "driver_id",
            "employee_id",
            "name",
            "phone_no",
            "email",
            "license_number",
            "license_expiry_date",
            "experience_years",
            "address",
            "status",
            "created_by",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "driver_id",
            "created_by",
            "created_at",
            "updated_at",
            "status",
        ]

    def validate_phone_no(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )
        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value

    def validate_experience_years(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Experience cannot be negative."
            )
        if value > 50:
            raise serializers.ValidationError(
                "Experience cannot exceed 50 years."
            )
        return value

    def validate_license_expiry_date(self, value):
        if value and value < timezone.now().date():
            raise serializers.ValidationError(
                "License has already expired."
            )
        return value


class DriverAssignmentSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(
        source="driver.name",
        read_only=True
    )
    employee_id = serializers.CharField(
        source="driver.employee_id",
        read_only=True
    )
    vehicle_id = serializers.IntegerField(
        source="vehicle_assignment.vehicle.id",
        read_only=True
    )
    registration_number = serializers.CharField(
        source="vehicle_assignment.vehicle.registration_number",
        read_only=True
    )
    assignment_id = serializers.IntegerField(
        source="vehicle_assignment.id",
        read_only=True
    )
    class Meta:
        model = DriverAssignment
        fields = [
            "id",
            "assignment_id",
            "driver",
            "driver_name",
            "employee_id",
            "vehicle_id",
            "registration_number",
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
            "assignment_id",
            "driver_name",
            "employee_id",
            "vehicle_id",
            "registration_number",
            "assigned_by",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                "End time must be after start time."
            )
        return attrs