from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from .views import APIReportDashBoard

urlpatterns = [
    url('dashboard/', APIReportDashBoard.as_view(), name="api-report-dashboard"),
]