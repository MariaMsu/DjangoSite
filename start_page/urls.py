from django.urls import path
from start_page import views

urlpatterns = [
    path('', views.auth),
    path('registration/', views.reg),
    path('verification/', views.verify),
]
