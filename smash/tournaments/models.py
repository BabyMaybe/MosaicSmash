from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Stats(models.Model):

    class Meta:
        verbose_name = "Stats"
        verbose_name_plural = "Stats"

    def __str__(self):
        pass

    wins = models.IntegerField(default=0)
    kos = models.IntegerField(default=0)
    falls = models.IntegerField(default=0)
    suicides = models.IntegerField(default=0)


class Icon(models.Model):

    class Meta:
        verbose_name = "Icon"
        verbose_name_plural = "Icons"

    def __str__(self):
        pass

    icon = models.ImageField(upload_to='icons/', height_field=icon_h, width_field=icon_w, null=True, blank=True)
    icon_h = models.IntegerField(null=True, blank=True, default=200)
    icon_w = models.IntegerField(null=True, blank=True, default=200)


class Player(models.Model):

    class Meta:
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return self.nickname

    user = models.OneToOneField(User)
    stats = models.OneToOneField(Stats)
    icon = models.OneToOneField(Icon, null=True, blank=True)
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)


class Character(models.Model):

    class Meta:
        verbose_name = "Character"
        verbose_name_plural = "Characters"

    def __str__(self):
        return self.name

    stats = models.OneToOneField(Stats)
    name = models.CharField(max_length=200)


class Pair(models.Model):

    class Meta:
        verbose_name = "Pair"
        verbose_name_plural = "Pairs"

    def __str__(self):
        pass

    stats = models.OneToOneField(Stats)
    player = models.OneToOneField(Player)
    character = models.OneToOneField(Character)


class Team(models.Model):

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        pass

    members = models.ManyToManyField(Pair)
    stats = models.OneToOneField(Stats)
    name = models.CharField(max_length=200, null=True, blank=True)


class Match(models.Model):

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        pass

    date_played = models.DateTimeField(auto_now_add=True)
    contestants = models.ManyToManyField(Pair)
    winner = models.OneToOneField(Pair)


class TeamMatch(models.Model):

    class Meta:
        verbose_name = "Team Match"
        verbose_name_plural = "Team Matches"

    def __str__(self):
        pass

    contestants = models.ManyToManyField(Team)
    winner = models.OneToOneField(Pair)


class Tournament(models.Model):

    class Meta:
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"

    def __str__(self):
        pass

    matches = models.ManyToManyField(Match)
    date_started = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(auto_now_add=False)

