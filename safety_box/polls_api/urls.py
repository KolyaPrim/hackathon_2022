from django.urls import path
from .views import PollsViewSet, PollsAPIViewSet

urlpatterns = [
    path("answer/", PollsAPIViewSet.as_view({'post': 'answer'})),
    path("<str:token>/", PollsViewSet.as_view({'get': 'get_poll'})),
]