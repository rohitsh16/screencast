from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib import messages
from django.conf import settings
from oth import models
import datetime
import json
from django.core import serializers
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .serializers import PlayerSerializer, levelSerializer
from .models import player, level


@api_view(['GET','POST'])

def index(request):
    event_date = datetime.datetime(2019, 8, 25, 22, 0, 0)

    if settings.MODE == 'PROD':
        if datetime.datetime.now() < event_date:
            return render(request, 'landing.html')

    lastlevel = settings.TOTAL_LEVELS

    user = request.user
    if user.is_authenticated:
        player = models.player.objects.get(user_id=request.user.pk)
        try:
            level = models.level.objects.get(l_number=player.current_level)
            return render(request, 'level.html', {'player': player, 'level': level})
        except models.level.DoesNotExist:
            if player.current_level > lastlevel:
                return render(request, 'win.html', {'player': player})
            return render(request, 'finish.html', {'player': player})

    return render(request, 'index_page.html')


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        profile = user
        try:
            player = models.player.objects.get(user=profile)
        except:
            player = models.player(user=profile)
            player.name = response.get('name')
            player.timestamp=datetime.datetime.now()
            player.save()
    elif backend.name == 'google-oauth2':
        profile = user
        try:
            player = models.player.objects.get(user=profile)
        except:
            player = models.player(user=profile)
            player.timestamp=datetime.datetime.now()
            player.name = response.get('name')['givenName'] + " " + response.get('name')['familyName']
            player.save()
            

@login_required
def answer(request):
    
    lastlevel = settings.TOTAL_LEVELS
    # print(lastlevel)

    ans = ""
    if request.method == 'POST':
        ans = request.POST.get('ans')
    player = models.player.objects.get(user_id=request.user.pk)
    try:
        level = models.level.objects.get(l_number=player.current_level)
    except models.level.DoesNotExist:
        if player.current_level > lastlevel:
            return render(request, 'win.html', {'player': player})
        return render(request, 'finish.html', {'player': player})
    # print answer
    # print level.answer
    if ans == level.answer:
        #print level.answer
        player.current_level = player.current_level + 1
        player.score = player.score + 10
        player.timestamp = datetime.datetime.now()
        level.numuser = level.numuser + 1
        level.accuracy = round(level.numuser/(float(level.numuser + level.wrong)),2)
        level.save()
        player.save()

        try:
            level = models.level.objects.get(l_number=player.current_level)
            return render(request, 'level_transition.html')

            return render(request, 'level.html', {'player': player, 'level': level})
        except:
            if player.current_level > lastlevel:
                return render(request, 'win.html', {'player': player}) 
            return render(request, 'finish.html', {'player': player})
    elif ans=="":
        pass 
        # messages.error(request, "Please enter answer!")

    else:
        level.wrong = level.wrong + 1
        level.save()

        messages.error(request, "Wrong Answer!, Try Again")

    return render(request, 'level.html', {'player': player, 'level': level})


def lboard(request):
    p = models.player.objects.order_by('-score','timestamp')
    cur_rank = 1

    for pl in p:
        pl.rank = cur_rank
        cur_rank += 1

    return render(request, 'lboard.html', {'players': p})

def rules(request):
    return render(request, 'index_page.html')

"""   API  """

def lboard_api(request):
    p = models.player.objects.order_by('-score','timestamp')
    current_rank = 1

    players_list = []

    for pl in p:
        pl.rank = current_rank
        players_list.append({
            'name':pl.name,
            'rank':pl.rank,
            'email':'',
            'score':pl.score,
        })
        current_rank += 1
    #In order to allow non-dict objects to be serialized set the safe parameter to False
    return Response(players_list,safe=False)


class PlayerList(APIView):
    def get(self,request,format=None):
        Player=player.objects.all()
        serializer=PlayerSerializer(Player, many=True)
        return Response(serializer.data)  

    def post(self,request,format=None):
        serializer=PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LevelList(APIView):
    def get(self,request,format=None):
        Level=level.objects.all()
        serializer=levelSerializer(Level,many=True)
        return Response(serializer.data)
