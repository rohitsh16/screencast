from django.contrib import admin
from .models import player, level, level2, level3, next_quiz_time
# Register your models here.

admin.site.register(player)
admin.site.register(level)
admin.site.register(level2)
admin.site.register(level3)
admin.site.register(next_quiz_time)