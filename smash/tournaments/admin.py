from django.contrib import admin

from .models import Player, Character, MatchEntry, Match, Tournament

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'icon']

class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

class MatchEntryAdmin(admin.ModelAdmin):
    list_display = ['player', 'character', 'team', 'kos', 'falls', 'winner']

class MatchAdmin(admin.ModelAdmin):
    list_display = ['date_played', 'teams', 'match_type', 'stage']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_started', 'date_ended', 'preliminary', 'winner']

admin.site.register(Player, PlayerAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(MatchEntry, MatchEntryAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tournament, TournamentAdmin)
