from django.urls import path
from .views import *

urlpatterns = [
    path("", healthAPIView.as_view(), name="health"),
    path("log/", LogProducerAPIView.as_view(), name="log-producer"),
]
