from rest_framework import serializers
from django.contrib.auth.models import User
from .models import player, level

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=player
        fields=("user","name","current_level","score","rank","timestamp")

class levelSerializer(serializers.ModelSerializer):
    #player=PlayerSerializer(many=True)
    class Meta:
        model=level
        fields=("l_number","text","answer","numuser","accuracy","wrong","hint")