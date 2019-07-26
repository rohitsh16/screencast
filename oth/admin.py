from django.contrib import admin
from .models import player, level, total_level
# Register your models here.

admin.site.register(player)
admin.site.register(level)
admin.site.register(total_level)