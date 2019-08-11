from django.contrib import admin
from .models.Level import Level
from .models.Player import Player
from .models.Question import Question

admin.site.register(Question)
admin.site.register(Level)
admin.site.register(Player)
