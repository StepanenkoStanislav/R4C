from django.urls import path, include

from api.views import add_robot


v1_urlpatterns = [
    path('add/', add_robot)
]


urlpatterns = [
    path('v1/', include(v1_urlpatterns))
]
