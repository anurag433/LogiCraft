from django.urls import path
from .views import (
    VehicleListCreateView,
    VehicleDetailView,
    VehicleAssignmentListCreateView,
    VehicleAssignmentDetailView,
    CompleteVehicleAssignmentView,
    MaintenanceListCreateView,
    MaintenanceDetailView,
    CompleteMaintenanceView,
)

urlpatterns = [
    path( "vehicles/", VehicleListCreateView.as_view(), name="vehicle-list-create"),
    path( "vehicles/<int:pk>/", VehicleDetailView.as_view(), name="vehicle-detail"),
    path("assignments/", VehicleAssignmentListCreateView.as_view(), name="assignment-list-create"),
    path( "assignments/<int:pk>/", VehicleAssignmentDetailView.as_view(), name="assignment-detail"),
    path( "assignments/<int:pk>/complete/", CompleteVehicleAssignmentView.as_view(), name="assignment-complete"),
    path( "maintenance/", MaintenanceListCreateView.as_view(), name="maintenance-list-create"),
    path( "maintenance/<int:pk>/", MaintenanceDetailView.as_view(), name="maintenance-detail"),
    path( "maintenance/<int:pk>/complete/", CompleteMaintenanceView.as_view(), name="maintenance-complete"),
]