from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from your_polls.models import Poll, Variant, Question


class PollsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    @xframe_options_exempt
    def get_poll(self, request: Request, token: str) -> Response:
        poll: Poll = get_object_or_404(Poll, id=int(token))
        poll_data = {
            "title": poll.title,
            "description": poll.description or "",
            # "css_file": poll.css_file.file,
            "questions": [
                {
                    "title": question.title,
                    "description": question.description or "",
                    "variants": [
                        {
                            "label": variant.label,
                            "type": variant.type,
                            "value": variant.value,
                            "name": variant.name
                        }
                        for variant
                        in Variant.objects.filter(question=question)
                    ]
                }
                for question
                in Question.objects.filter(poll=poll)
            ]
        }
        return Response({"poll": poll_data}, template_name='poll.html')
