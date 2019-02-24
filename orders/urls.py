from django.urls import path

from . import views

# Add namespace to URLconf
app_name = 'orders'

urlpatterns = [

    # ex: /
    path('', views.IndexView.as_view(), name='index'),

    # ex: /1
    path('<int:pk>/', views.DetailView.as_view(), name='details'),
]
