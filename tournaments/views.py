from django.shortcuts import render
from django.db.models import Sum, Max, Min, Count
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from django.http import HttpResponse

from .models import MatchEntry, Tournament, Match, Player
from .forms import SignupForm, DataEntryForm, MatchForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
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
        context['matches'] = Match.objects.filter(tournament=self.get_object()).order_by('date_played')
        return context


class ResultsView(DetailView):
    model = Match
    template_name = 'tournaments/match_results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['results'] = MatchEntry.objects.filter(match=self.get_object()).order_by('-kos')
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
        context['points'] = context['kos'] - context['falls']
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



# EntryFormSet = modelformset_factory(MatchEntry, form=DataEntryForm, extra=4, max_num=8)
EntryFormSet = inlineformset_factory(Match, MatchEntry, can_delete=False, extra=4, max_num=8, form=DataEntryForm)


class DataEntryView(UserPassesTestMixin, CreateView):
    model = MatchEntry
    form_class = DataEntryForm
    template_name = 'tournaments/tournament_entry.html'
    login_url = '/tournaments/' #no way to login except through admin pannel rn so send back to list
    redirect_unauthenticated_users = True

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(DataEntryView, self).get_context_data(**kwargs)
        context['formset'] = EntryFormSet(queryset=MatchEntry.objects.filter(kos__lt=0), initial=[{'kos': None, 'falls': None} for x in range(4)])
        context['match'] = MatchForm()
        context['tournament_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        print(args)
        print( kwargs)
        form = MatchForm(request.POST)

        if form.is_valid():
            match = form.save(commit=False)
            match.tournament = Tournament.objects.get(pk=kwargs['pk'])
            match.save()

            entries = EntryFormSet(request.POST, instance=match)

            for entry in entries:
                if entry.is_valid():
                    data_point = entry.save(commit=False)
                    data_point.match = match
                    data_point.save()
                    data_point.player.save()

            return redirect('/tournaments/%s' % match.tournament.pk)

        return redirect('/tournaments/%s/data_entry' % kwargs['pk'])
