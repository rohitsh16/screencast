from django.contrib import admin
from .models import player, level, level2, level3, player_level
# Register your models here.

admin.site.register(player)
admin.site.register(level)
admin.site.register(level2)
admin.site.register(level3)
admin.site.register(player_level)