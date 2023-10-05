from django.urls import path

from robots.views import download_robots_summary


urlpatterns = [
    path('download-robots-summary/', download_robots_summary)
]
