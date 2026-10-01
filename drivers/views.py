from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from fleet.models import Vehicle
from .filters import DriverFilter
from .models import Driver, DriverAssignment
from .permissions import IsAdminOrFleetManager
from .serializers import (DriverAssignmentSerializer,DriverSerializer,
)
from .services import (
    assign_driver_to_vehicle,
    complete_driver_assignment,
    create_driver,
    deactivate_driver,
)

class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all().order_by("-created_at")
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrFleetManager]
    filterset_class = DriverFilter
    search_fields = [
        "driver_id",
        "employee_id",
        "name",
        "phone_no",
        "license_number",
    ]
    ordering_fields = [
        "created_at",
        "name",
        "experience_years",
        "status",
    ]

    def perform_create(self, serializer):
        driver = create_driver(
            validated_data=serializer.validated_data,
            created_by=self.request.user
        )
        serializer.instance = driver

class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrFleetManager]
    def perform_destroy(self, instance):
        deactivate_driver(instance)

class AvailableDriverListView(generics.ListAPIView):
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrFleetManager]
    def get_queryset(self):
        return Driver.objects.filter(
            status=Driver.Status.AVAILABLE
        ).order_by("name")

class DriverAssignmentListView(generics.ListAPIView):
    serializer_class = DriverAssignmentSerializer
    permission_classes = [
        IsAdminOrFleetManager
    ]
    def get_queryset(self):
        driver_id = self.kwargs["driver_id"]
        return DriverAssignment.objects.filter(
            driver_id=driver_id
        ).select_related(
            "driver",
            "vehicle_assignment",
            "vehicle_assignment__vehicle"
        )
class DriverAssignView(APIView):
    permission_classes = [IsAdminOrFleetManager ]
    def post(self, request, driver_id):
        driver = get_object_or_404(
            Driver,
            id=driver_id
        )
        vehicle_id = request.data.get("vehicle_id")
        if not vehicle_id:
            return Response(
                {
                    "detail": "vehicle_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        vehicle = get_object_or_404(
            Vehicle,
            id=vehicle_id
        )

        start_time = request.data.get(
            "start_time"
        )

        notes = request.data.get(
            "notes",
            ""
        )

        if start_time:
            from django.utils.dateparse import parse_datetime

            start_time = parse_datetime(start_time)

            if not start_time:
                return Response(
                    {
                        "detail": "Invalid start_time format."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        assignment = assign_driver_to_vehicle(
            driver=driver,
            vehicle=vehicle,
            assigned_by=request.user,
            start_time=start_time,
            notes=notes
        )

        serializer = DriverAssignmentSerializer(
            assignment
        )

        return Response(
            {
                "message": "Driver assigned to vehicle successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class DriverCompleteAssignmentView(APIView):

    permission_classes = [
        IsAdminOrFleetManager
    ]
    def post(self, request, assignment_id):

        assignment = get_object_or_404(
            DriverAssignment,
            id=assignment_id
        )

        driver_assignment = complete_driver_assignment(
            assignment
        )

        serializer = DriverAssignmentSerializer(
            driver_assignment
        )
        return Response(
            {
                "message": "Driver assignment completed successfully.",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )