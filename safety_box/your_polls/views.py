import datetime
import logging

import importlib
import traceback

from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from .models import *


class PollViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    def get_poll_list(self, request):
        user = request.user
        queryset = Poll.objects.filter(author_id=user.id)
        poll_list = [item for item in queryset]
        return Response(data={'polls': poll_list,
                              'item_template': 'polls_item.html'},
                        template_name='polls_list.html')

    def create_poll(self, request):
        return Response(template_name='poll_creating_page.html')
