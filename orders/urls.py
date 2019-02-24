from django.urls import path

from . import views

# Add namespace to URLconf
app_name = 'orders'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index")
]
