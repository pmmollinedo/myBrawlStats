from django.urls import path
from my_brawl_stats import views

urlpatterns = [
    path('', views.home, name="home")
]