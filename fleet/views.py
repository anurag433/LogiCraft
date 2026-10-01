from rest_framework import generics, status
from rest_framework.response import Response
from .models import (Vehicle,VehicleAssignment,VehicleMaintenance)
from .permissions import IsAdminOrFleetManager
from .serializers import (VehicleSerializer,VehicleAssignmentSerializer,VehicleMaintenanceSerializer)

from .services import (assign_vehicle,complete_assignment,start_maintenance,complete_maintenance)

class VehicleListCreateView(generics.ListCreateAPIView):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrFleetManager]
    def perform_create(self, serializer):
        serializer.save()

class VehicleDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrFleetManager]

class VehicleAssignmentListCreateView(generics.ListCreateAPIView):

    queryset = VehicleAssignment.objects.select_related(
        "vehicle",
        "assigned_by"
    )
    serializer_class = VehicleAssignmentSerializer
    permission_classes = [IsAdminOrFleetManager]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(
            raise_exception=True
        )
        data = serializer.validated_data
        try:
            assignment = assign_vehicle(
                vehicle=data["vehicle"],
                assigned_by=request.user,
                start_time=data["start_time"],
                end_time=data.get("end_time"),
                notes=data.get("notes", "")
            )
        except ValueError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = (
            self.get_serializer(assignment)
        )
        return Response(
            {
                "success": True,
                "message": "Vehicle assigned successfully.",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class VehicleAssignmentDetailView(generics.RetrieveAPIView):
    queryset = VehicleAssignment.objects.select_related(
        "vehicle",
        "assigned_by"
    )
    serializer_class = VehicleAssignmentSerializer
    permission_classes = [IsAdminOrFleetManager]

class CompleteVehicleAssignmentView(generics.GenericAPIView):

    queryset = VehicleAssignment.objects.all()
    serializer_class = VehicleAssignmentSerializer
    permission_classes = [IsAdminOrFleetManager]

    def post(self, request, pk):
        try:
            assignment = self.get_object()
            assignment = complete_assignment(
                assignment
            )
        except ValueError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(assignment)

        return Response({
            "success": True,
            "message": (
                "Vehicle assignment completed."
            ),
            "data": serializer.data
        })


class MaintenanceListCreateView(generics.ListCreateAPIView):

    queryset = VehicleMaintenance.objects.select_related(
        "vehicle",
        "created_by"
    )
    serializer_class = VehicleMaintenanceSerializer
    permission_classes = [IsAdminOrFleetManager]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        vehicle = data.pop("vehicle")
        try:
                maintenance = start_maintenance(
                vehicle=vehicle,
                maintenance_data=data,
                created_by=request.user
            )
        except ValueError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        response_serializer = (
            self.get_serializer(maintenance)
        )
        return Response(
            {
                "success": True,
                "message": (
                    "Maintenance scheduled successfully."
                ),
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class MaintenanceDetailView(generics.RetrieveAPIView):
    queryset = VehicleMaintenance.objects.select_related(
        "vehicle",
        "created_by"
    )
    serializer_class = VehicleMaintenanceSerializer
    permission_classes = [IsAdminOrFleetManager]

class CompleteMaintenanceView(generics.GenericAPIView):

    queryset = VehicleMaintenance.objects.all()
    serializer_class = VehicleMaintenanceSerializer
    permission_classes = [IsAdminOrFleetManager]
    def post(self, request, pk):
        try:
            maintenance = self.get_object()
            maintenance = complete_maintenance(maintenance)
        except ValueError as error:
            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(
            maintenance
        )
        return Response({
            "success": True,
            "message": (
                "Vehicle maintenance completed."
            ),
            "data": serializer.data
        })