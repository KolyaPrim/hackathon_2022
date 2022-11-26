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

    def get_poll(self, request, poll_id: int):
        poll: Poll = get_object_or_404(Poll, id=poll_id)
        poll_data = {
            "title": poll.title,
            "description": poll.description or "",
            "css_file": poll.css_file.file,
            "questions": [
                {
                    "title": question.title,
                    "description": question.description or "",
                    "variants": [
                        {
                            "label": variant.label,
                            "type": variant.type,
                            "value": variant.value,
                            "name": variant.name,
                            "id": variant.id
                        }
                        for variant
                        in Variant.objects.filter(question=question)
                    ]
                }
                for question
                in Question.objects.filter(poll=poll)
            ]
        }
        return Response(data={'poll': poll_data},
                        template_name='poll_page.html')
