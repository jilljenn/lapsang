from django.contrib import admin
from lapsang.models import Game


class GameAdmin(admin.ModelAdmin):
    raw_id_fields = ('sentences',)


admin.site.register(Game, GameAdmin)
