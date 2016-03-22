from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.

class Player(models.Model):

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return self.nickname

    user = models.OneToOneField(User)
    icon = models.ImageField(upload_to='player_icons', null=True, blank=True)
    nickname = models.CharField(max_length=200)
    kos = models.IntegerField(default=0)
    falls = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if MatchEntry.objects.filter(player=self):
            self.kos = MatchEntry.objects.filter(player=self).aggregate(kos=Sum('kos'))['kos']
            self.falls = MatchEntry.objects.filter(player=self).aggregate(falls=Sum('falls'))['falls']
            self.wins = MatchEntry.objects.filter(player=self).filter(winner=True).count()
            self.losses = MatchEntry.objects.filter(player=self).filter(winner=False).count()
        super(Player, self).save(*args, **kwargs)



class Character(models.Model):

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='char_icons', null=True, blank=True)


class Tournament(models.Model):

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, null=True, blank=True)
    date_started = models.DateField(default=timezone.now)
    date_ended = models.DateField(null=True, blank=True)
    preliminary = models.BooleanField(default=False)
    winner = models.ForeignKey(Player, null=True, blank=True)


class Match(models.Model):

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        return self.name

    #Choices for team battles
    STOCK = "Stock"
    TIME = "Time"
    COIN = "Coin"

    MATCH_TYPE = (
        (STOCK, "Stock Match"),
        (TIME, "Time Match"),
        (COIN, "Coin Match"),
        )
#Choices for stages

    STAGE_CHOICES = (
        ('75m', '75m'),
        ('Battlefield', 'Battlefield'),
        ('Big Battlefield', 'Big Battlefield'),
        ('Boxing Ring', 'Boxing Ring'),
        ('Bridge of Eldin', 'Bridge of Eldin'),
        ('Castle Siege', 'Castle Siege'),
        ('Coliseum', 'Coliseum'),
        ('Delfino Plaza', 'Delfino Plaza'),
        ('Duck Hunt', 'Duck Hunt'),
        ('Final Destination', 'Final Destination'),
        ('Flat Zone X', 'Flat Zone X'),
        ('Gamer', 'Gamer'),
        ('Garden of Hope', 'Garden of Hope'),
        ('Gaur Plains', 'Gaur Plains'),
        ('Halberd', 'Halberd'),
        ('Jungle Hijinxs', 'Jungle Hijinxs'),
        ('Kalos Pokemon League', 'Kalos Pokemon League'),
        ('Kongo Jungle 64', 'Kongo Jungle 64'),
        ('Luigi\'s Mansion', 'Luigi\'s Mansion'),
        ('Lylat Cruise', 'Lylat Cruise'),
        ('Mario Circuit', 'Mario Circuit'),
        ('Mario Galaxy', 'Mario Galaxy'),
        ('Mushroom Kingdom U', 'Mushroom Kingdom U'),
        ('Norfair', 'Norfair'),
        ('Onett', 'Onett'),
        ('Orbital Gate Assault', 'Orbital Gate Assault'),
        ('Pac-Land', 'Pac-Land'),
        ('Palutena\'s Temple', 'Palutena\'s Temple'),
        ('Pilot Wings', 'Pilot Wings'),
        ('Pokemon Stadium 2', 'Pokemon Stadium 2'),
        ('Port Town Aero Dive', 'Port Town Aero Dive'),
        ('Pyrosphere', 'Pyrosphere'),
        ('Skyloft', 'Skyloft'),
        ('Skyworld', 'Skyworld'),
        ('Smashville', 'Smashville'),
        ('Temple', 'Temple'),
        ('The Great Cave Offensive', 'The Great Cave Offensive'),
        ('Town and City', 'Town and City'),
        ('Wii Fit Studio', 'Wii Fit Studio'),
        ('Wily Castle', 'Wily Castle'),
        ('Windy Hill', 'Windy Hill'),
        ('Woolly World', 'Woolly World'),
        ('Wrecking Crew', 'Wrecking Crew'),
        ('Wuhu Island', 'Wuhu Island'),
        ('Yoshi\'s Island', 'Yoshi\'s Island'),
        )

    name = models.CharField(max_length=200)
    date_played = models.DateTimeField(default=timezone.now)
    tournament = models.ForeignKey(Tournament)
    teams = models.BooleanField(default=False)
    match_type = models.CharField(max_length=100, choices=MATCH_TYPE, default=STOCK)
    time_length = models.IntegerField(default=3)
    stage = models.CharField(max_length=100, choices=STAGE_CHOICES, default="Final Destination")
    winner = models.ForeignKey(Player, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            round = 'Round '
            round_no = self.tournament.match_set.count()
            print (round_no)
            self.name = round + str(round_no)
        super(Match, self).save(*args, **kwargs)

class MatchEntry(models.Model):

    class Meta:
        verbose_name = "Match Entry"
        verbose_name_plural = "Match Entries"

    #Choices for team battles
    SOLO = 0
    TEAM1 = 1
    TEAM2 = 2
    TEAM3 = 3
    TEAM_CHOICES = (
        (SOLO, "Solo"),
        (TEAM1, "Team 1"),
        (TEAM2, "Team 2"),
        (TEAM3, "Team 3")
        )

    match = models.ForeignKey(Match)
    player = models.ForeignKey(Player)
    character = models.ForeignKey(Character)
    team = models.IntegerField(choices=TEAM_CHOICES, default=SOLO)
    kos = models.IntegerField(default=0)
    falls = models.IntegerField(default=0)
    winner = models.BooleanField(default=False)





