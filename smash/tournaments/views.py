from django.shortcuts import render

from django.views.generic import ListView, DetailView

from .models import MatchEntry, Tournament, Match

# Create your views here.
class ResultsView(DetailView):
    model = Match
    template_name = 'tournaments/match_results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['results'] = MatchEntry.objects.filter(match=self.get_object())
        return context


class TournamentsView(ListView):
    model = Tournament
    template_name = 'tournaments/tournament_list.html'

class MatchesView(DetailView):
    model = Tournament
    template_name = 'tournaments/match_list.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesView, self).get_context_data(**kwargs)
        context['matches'] = Match.objects.filter(tournament=self.get_object())
        return context

