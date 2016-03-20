from __future__ import unicode_literals

from django.db import models
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

    #Choices for team battles
    STOCK = "Stock"
    TIME = "Time"
    COIN = "Coin"

    MATCH_TYPE = (
        (STOCK, "Stock Match"),
        (TIME, "Time Match"),
        (COIN, "Coin Match"),
        )

    STAGE_CHOICES = (
        (0,'75m'),
        (1,'Battlefield'),
        (2,'Big Battlefield'),
        (3,'Boxing Ring'),
        (4,'Bridge of Eldin'),
        (5,'Castle Siege'),
        (6,'Coliseum'),
        (7,'Delfino Plaza'),
        (8,'Duck Hunt'),
        (9,'Final Destination'),
        (10,'Flat Zone X'),
        (11,'Gamer'),
        (12,'Garden of Hope'),
        (13,'Gaur Plains'),
        (14,'Halberd'),
        (15,'Jungle Hijinxs'),
        (16,'Kalos Pokémon League'),
        (17,'Kongo Jungle 64'),
        (18,'Luigi\'s Mansion'),
        (19,'Lylat Cruise'),
        (20,'Mario Circuit'),
        (21,'Mario Galaxy'),
        (22,'Mushroom Kingdom U'),
        (23,'Norfair'),
        (24,'Onett'),
        (25,'Orbital Gate Assault'),
        (26,'Pac-Land'),
        (27,'Palutena\'s Temple'),
        (28,'Pilot Wings'),
        (29,'Pokémon Stadium 2'),
        (30,'Port Town Aero Dive'),
        (31,'Pyrosphere'),
        (32,'Skyloft'),
        (33,'Skyworld'),
        (34,'Smashville'),
        (35,'Temple'),
        (36,'The Great Cave Offensive'),
        (37,'Town and City'),
        (38,'Wii Fit Studio'),
        (39,'Wily Castle'),
        (40,'Windy Hill'),
        (41,'Woolly World'),
        (42,'Wrecking Crew'),
        (43,'Wuhu Island'),
        (44,'Yoshi\'s Island'),
        )

    date_played = models.DateTimeField(default=timezone.now)
    tournament = models.ForeignKey(Tournament)
    teams = models.BooleanField(default=False)
    match_type = models.CharField(max_length=100, choices=MATCH_TYPE, default=STOCK)
    time_length = models.IntegerField(default=3)
    stage = models.IntegerField(choices=STAGE_CHOICES, default=9) #9 sets default stage to Final Destination
                                                                  #I just didnt want to make 45 constants :(

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



