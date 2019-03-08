from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# Add namespace to URLconf
app_name = 'orders'

urlpatterns = [

    # ex: /
    path('', views.IndexView.as_view(), name='index'),

    # ex: /1
    path('<int:pk>/', views.DetailView.as_view(), name='details'),

    # ex: /login
    path('login/', views.login_view, name='login'),

    # ex: /signup
    path('signup/', views.signup_view, name='signup'),
]
