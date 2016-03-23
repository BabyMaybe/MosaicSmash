from django.shortcuts import render
from django.db.models import Sum, Max, Min, Count
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.forms import formset_factory

from .models import MatchEntry, Tournament, Match, Player
from .forms import SignupForm, DataEntryForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# Create your views here.
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


class ResultsView(DetailView):
    model = Match
    template_name = 'tournaments/match_results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['results'] = MatchEntry.objects.filter(match=self.get_object())
        return context

class ProfileView(DetailView):
    model = Player
    template_name = 'tournaments/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        player_matches = MatchEntry.objects.filter(player=self.get_object())
        context['wins'] = player_matches.filter(winner=True).count()
        context['losses'] = player_matches.filter(winner=False).count()
        context['kos'] = player_matches.aggregate(kos=Sum('kos'))['kos']
        context['falls'] = player_matches.aggregate(falls=Sum('falls'))['falls']
        context['tournaments_won'] = Tournament.objects.filter(winner=self.get_object()).count()
        context['joined'] = self.get_object().user.date_joined
        matches = Match.objects.filter(matchentry__player=self.get_object())
        context['last_match'] = matches.aggregate(last=Max('date_played'))['last']
        return context

class LeaderboardView(ListView):
    model = Player
    template_name = 'tournaments/leaderboard.html'

    def get_context_data(self, **kwargs):
        context = super(LeaderboardView, self).get_context_data(**kwargs)
        context['players'] = Player.objects.order_by('-kos', 'falls')
        Player.objects.update()
        return context

class SignupView(FormView):
    model = User
    form_class = SignupForm
    template_name = 'tournaments/signup.html'

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if (form.is_valid()):
            print('valid form received')
            f = form.cleaned_data

            username = f['username']
            email = f['email']
            password = f['password']
            first = f['first_name']
            last = f['last_name']

            new_user = User.objects.create_user(username, email, password, first_name=first, last_name=last )
            new_player = Player.objects.create(user=new_user, nickname=username)
            user = authenticate(username=username, password=password)
            # login (self.request, user)

            # return redirect('/leaderboard', user_id=user.id)
            return redirect('/leaderboard')

        return redirect('/signup/')

    def get_success_url(self):
        return reverse('profile/',args=(self.object.id,))

class DataEntryView(FormView):
    model = MatchEntry
    form_class = DataEntryForm
    template_name = 'tournaments/tournament_entry.html'

    def get_context_data(self, **kwargs):
        context = super(DataEntryView, self).get_context_data(**kwargs)
        context['formset'] = formset_factory(DataEntryForm, extra=4, max_num=8)
        return context
