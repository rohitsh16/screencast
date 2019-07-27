from django.contrib import admin
from .models import player, level, total_level, next_quiz_time
# Register your models here.

admin.site.register(player)
admin.site.register(level)
admin.site.register(total_level)
admin.site.register(next_quiz_time)