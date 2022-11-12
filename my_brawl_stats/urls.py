from django.urls import path
from my_brawl_stats import views

app_name = 'my_brawl_stats'

urlpatterns = [
    # views
    path('', views.home, name="home"),
    path('brawler/<int:brawlerId>', views.brawler, name="brawler"),
    path('settings', views.settings, name="settings"),
    # ajax
    path('api', views.api, name="api")
]