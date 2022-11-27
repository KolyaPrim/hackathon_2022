from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from analytics.plotter import AnalyticsPlotter
from your_polls.models import Poll


# Create your views here.


class AnalyticsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    def get_analytics_template(self, request: Request, poll_id: int) -> Response:
        poll = get_object_or_404(Poll, id=poll_id)
        plotter = AnalyticsPlotter(poll)
        app_name = plotter.build_analytics_app()
        return Response(data={
            "analytics_app": app_name
        }, template_name="analytics.html")
