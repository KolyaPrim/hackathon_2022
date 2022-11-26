from django.urls import path
from .views import PollsViewSet

urlpatterns = [
    path("<str:token>/", PollsViewSet.as_view({'get': 'get_poll'}))
]