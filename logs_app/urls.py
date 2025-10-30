from django.urls import path
from .views import *

urlpatterns = [
    path("log/", LogProducerAPIView.as_view(), name="log-producer"),
]
