from django.urls import path
from .views import DriverListCreateView, DriverRetrieveUpdateDeleteView, AdminProfileView

urlpatterns = [
    path('drivers/', DriverListCreateView.as_view(), name='driver-list-create'),
    path('drivers/<int:pk>/', DriverRetrieveUpdateDeleteView.as_view(), name='driver-detail'),
]
