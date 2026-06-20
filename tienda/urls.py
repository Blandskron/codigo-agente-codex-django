from django.urls import path

from .views import inicio

app_name = "tienda"

urlpatterns = [
    path("", inicio, name="inicio"),
]
