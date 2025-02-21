from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
]