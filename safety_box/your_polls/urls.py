from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

from .views import PollViewSet

urlpatterns = [
    path('', PollViewSet.as_view({'get': 'get_poll_list'})),
    path('poll/<int:poll_id>/', PollViewSet.as_view({'get': 'get_poll'})),
    path('creating_poll/', PollViewSet.as_view({'get': 'create_poll'})),
    path('save_poll/', PollViewSet.as_view({'post': 'save_poll'})),
]
