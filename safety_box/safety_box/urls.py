from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView


from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
    path('', include('your_polls.urls')),
    path('accounts/', include('allauth.urls')),
    path('logout', LogoutView.as_view()),
    path('api/', include('polls_api.urls')),
    path('analytics/', include('analytics.urls')),
    *([
          re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
          re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
      ] if not settings.DEBUG else [])
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)