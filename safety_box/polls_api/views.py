from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response


class PollsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    @xframe_options_exempt
    def get_poll(self, request: Request, token: str) -> Response:
        return Response(template_name='poll.html')
