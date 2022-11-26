import datetime
import logging

import importlib
import traceback

from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect
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
        try:
            css_file = poll.css_file.file
        except:
            css_file = None
        poll_data = {
            'id': poll.id,
            "title": poll.title,
            "description": poll.description or "",
            "css_file": css_file,
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

    def save_poll(self, request):
        # data = request.data
        data = {
            'title': "Великий опрос",
            'description': "Описание великого опроса",
            'questions': [
                {
                    "text": "Любите ли вы котиков?",
                    "description": "Все мы любим котиков",
                    "variants": [
                        {
                            "label": "Да",
                            "type": "radiobutton"
                        },
                        {
                            "label": "Тоже да",
                            "type": "radiobutton"
                        }
                    ]
                },
                {
                    "text": "Каких котиков вы любите?",
                    "variants": [
                        {
                            "label": "Рыжих",
                            "type": "checkbox"
                        },
                        {
                            "label": "Чёрных",
                            "type": "checkbox"
                        },
                        {
                            "label": "Белых",
                            "type": "checkbox"
                        },
                        {
                            "label": "Серых",
                            "type": "checkbox"
                        },
                        {
                            "label": "Разноцветных",
                            "type": "checkbox"
                        },
                        {
                            "label": "Сфинксов",
                            "type": "checkbox"
                        }
                    ]
                }
            ]
        }
        poll_obj = Poll(title=data.get('title'), description=data.get('description', ''), author=request.user)
        poll_obj.save()

        questions = data.get('questions')

        for index_q, question in enumerate(questions):
            question_obj = Question(title=question.get('text'), description=question.get('description', ''),
                                    poll=poll_obj)
            question_obj.save()

            variants = question.get('variants')

            for index_v, variant in enumerate(variants):
                value = ''
                if variant.get('type') in ('radio', 'checkbox'):
                    value = index_v

                variant_obj = Variant(label=variant.get("label"), type=variant.get('type'), value=value, name=index_q,
                                      question=question_obj)
                variant_obj.save()

        return redirect("/poll/" + str(poll_obj.id) + "/")
