import time

import dash
from django_plotly_dash import DjangoDash

from analytics.models import PollsGet
from your_polls.models import Poll, Question, Variant, Answer
import pandas as pd
import plotly.express as px


class AnalyticsPlotter:
    def __init__(self, poll: Poll):
        self.poll = poll

    def build_analytics_app(self) -> str:
        poll_views = PollsGet.objects.filter(poll=self.poll)
        poll_views_pd = pd.DataFrame([
            {"date":poll_view.datetime}
            for poll_view
            in poll_views])
        poll_views_pd['date'] = poll_views_pd['date'].round("d")
        poll_views_by_dates = poll_views_pd.groupby('date')['date'].count()
        poll_views_by_dates = pd.DataFrame({'date': poll_views_by_dates.index,'count': poll_views_by_dates})

        questions = Question.objects.filter(poll=self.poll)
        questions_data = {
            question.title: [
                {
                    'id': variant.id,
                    'label':variant.label,
                    'count': len(Answer.objects.filter(variant=variant))
                }
                for variant
                in Variant.objects.filter(question=question)
                if variant.type != 'text'
            ]
            for question
            in questions
        }
        questions_graphs = [
            dash.html.Div([
                dash.html.H1(question_title),
                dash.dcc.Graph(
                    figure=self.generate_question_bar(variants_data)
                )
            ])
            for question_title, variants_data
            in questions_data.items()
        ]

        name = str(time.time()).replace('.','')
        app = DjangoDash(name=name)
        app.layout = dash.html.Div([
            dash.html.H1('Slice of visits by dates'),
            dash.dcc.Graph(
                figure=px.line(poll_views_by_dates, x="date", y="count", markers=True)
            ),
            *questions_graphs
        ])

        return name

    def generate_question_bar(self, variants_data):
        fig = px.bar(
                        pd.DataFrame(
                            variants_data
                        ),
                        x='id',
                        y='count',
                        text="label"
                    )
        fig.update_xaxes(visible=False, showticklabels=False)
        return fig
