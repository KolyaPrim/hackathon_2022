from django.urls import path
from .views import AnalyticsViewSet

urlpatterns = [
    path("<int:poll_id>/", AnalyticsViewSet.as_view({'get': 'get_analytics_template'})),
]