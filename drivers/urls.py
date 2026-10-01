from django.urls import path

from .views import (
    AvailableDriverListView,
    DriverAssignView,
    DriverAssignmentListView,
    DriverCompleteAssignmentView,
    DriverDetailView,
    DriverListCreateView,
)
urlpatterns = [

    path( "", DriverListCreateView.as_view(), name="driver-list-create" ),
    path( "available/", AvailableDriverListView.as_view(), name="available-drivers" ),
    path( "<int:driver_id>/", DriverDetailView.as_view(), name="driver-detail" ),
    path( "<int:driver_id>/assignments/", DriverAssignmentListView.as_view(), name="driver-assignments"),
    path( "<int:driver_id>/assign/", DriverAssignView.as_view(), name="driver-assign"),
    path( "assignments/<int:assignment_id>/complete/", DriverCompleteAssignmentView.as_view(), name="driver-assignment-complete" ),
]