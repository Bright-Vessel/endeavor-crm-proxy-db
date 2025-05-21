from django.urls import path
from .views import AvailabilitySlotListView

urlpatterns = [
    path('api/schools/<int:crm_id>/availability/', AvailabilitySlotListView.as_view()),
]
