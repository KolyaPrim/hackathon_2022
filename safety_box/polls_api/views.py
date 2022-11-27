import hashlib
import json
import time

from django.shortcuts import render, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from analytics.models import PollsGet, UserHash
from your_polls.models import Poll, Variant, Question, Answer


class PollsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    @xframe_options_exempt
    def get_poll(self, request: Request, token: str) -> Response:
        poll: Poll = get_object_or_404(Poll, id=int(token))
        PollsGet(poll=poll).save()
        poll_data = {
            "title": poll.title,
            "description": poll.description or "",
            "id": poll.id,
            # "css_file": poll.css_file.file,
            "questions": [
                {
                    "title": question.title,
                    "description": question.description or "",
                    "id": question.id,
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
        return Response({"poll": poll_data}, template_name='poll.html')


class PollsAPIViewSet(viewsets.ViewSet):
    renderer_classes = [JSONRenderer]

    def answer(self, request: Request) -> Response:
        answers = json.loads(dict(request.data)['inputs_data'][0])
        time_hash = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
        user_hash = UserHash(user_hash=time_hash)
        user_hash.save()
        for answer in answers:
            Answer(value=answer["value"], variant_id=answer["id"], user_hash=user_hash).save()
            pass
        return Response()
