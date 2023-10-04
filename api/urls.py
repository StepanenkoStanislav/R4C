from django.urls import path

from api.views import add_robot


urlpatterns = [
    path('add/', add_robot)
]
