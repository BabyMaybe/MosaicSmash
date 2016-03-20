from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import MatchEntry

# Create your views here.
class ResultsView(ListView):
    model = MatchEntry
    template_name = 'tournaments/match_results.html'

    # def get_context_data(self, **kwargs):


