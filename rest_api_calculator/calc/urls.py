from django.conf.urls import url

from .views import StandardCalculator, ScientificCalculator

urlpatterns = [
    url('standard/', StandardCalculator.as_view(), name="standard-calculator"),
    url('scientific/', ScientificCalculator.as_view(), name="scientific-calculator"),
]
