from django.urls import path

from .views import PollViewSet, PollsOperatingObjectApi

urlpatterns = [
    path('', PollViewSet.as_view({'get': 'get_poll_list'})),
    path('poll/<int:poll_id>/', PollViewSet.as_view({'get': 'get_poll'})),
    path('creating_poll/', PollViewSet.as_view({'get': 'create_poll'})),
    path('save_poll/', PollsOperatingObjectApi.as_view({'post': 'save_poll'})),
    path('poll/delete/<int:poll_id>/', PollsOperatingObjectApi.as_view({'post': 'delete_poll'})),
]
