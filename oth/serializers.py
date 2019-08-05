from rest_framework import serializers
from django.contrib.auth.models import User
from .models import player, level1, level2, level3

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=player
        fields=("user","name","current_level","score","rank","timestamp")

class levelSerializer1(serializers.HyperlinkedModelSerializer):
    #player=PlayerSerializer(many=True)
    class Meta:
        model=level1
        fields=("l_number","image","audio","text","answer","numuser","accuracy","wrong","hint")


class levelSerializer2(serializers.HyperlinkedModelSerializer):
    #player=PlayerSerializer(many=True)
    class Meta:
        model=level2
        fields=("l_number","image","audio","text","answer","numuser","accuracy","wrong","hint")



class levelSerializer3(serializers.HyperlinkedModelSerializer):
    #player=PlayerSerializer(many=True)
    class Meta:
        model=level3
        fields=("l_number","image","audio","text","answer","numuser","accuracy","wrong","hint")
