from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from .serializers import PlayerSerializer, levelSerializer1, levelSerializer2, levelSerializer3
from .models import player, level, level2, level3, player_level


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
    
    time1 = False
    time2 = False
    CurrentDate = datetime.datetime.now()
    ExpectedDate1 = "5/8/2019 17:12"
    ExpectedDate2 = "5/8/2019 17:15"
    ExpectedDate1 = datetime.datetime.strptime(ExpectedDate1, "%d/%m/%Y %H:%M")
    ExpectedDate2 = datetime.datetime.strptime(ExpectedDate2, "%d/%m/%Y %H:%M")
    if CurrentDate > ExpectedDate1:
        time1 = True

    if CurrentDate > ExpectedDate2:
        time2 = True
    
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
        #player.current_level = player.current_level + 1
        player.current_question = player.current_question + 1
        player.score = player.score + 10
        player.timestamp = datetime.datetime.now()
        level.numuser = level.numuser + 1
        level.accuracy = round(level.numuser/(float(level.numuser + level.wrong)),2)
        level.save()
        player.save()
        
        try:
            level = models.level.objects.get(l_number=player.current_question)
            #return render(request, 'level_transition.html')
            if player.current_level == 1:
                return render(request, 'level.html', {'player': player, 'level': level})

            elif player.current_level == 2:
                return render(request, 'level.html', {'player': player, 'level': level2})

            elif player.current_level == 3:
                return render(request, 'level.html', {'player': player, 'level': level3})
            
        except:
            if player.current_level > lastlevel:
                return render(request, 'win.html', {'player': player}) 
            return render(request, 'finish.html', {'player': player})
        '''
        try:
            level = models.level.objects.get(l_number=player.current_level)
            #return render(request, 'level_transition.html')

            if player.current_level <= 2:
                return render(request, 'level.html', {'player': player, 'level': level})

            if player.current_level > 2 and time1 == False:
                return render(request, 'finish.html', {'player': player})

            if player.current_level > 2 and player.current_level <= 4 and time1 == True:  
                return render(request, 'level.html', {'player': player, 'level': level})
               
            if player.current_level >= 4 and time2 == False: 
                return render(request, 'finish.html', {'player': player}) 

            if player.current_level >= 4 and player.current_level < 6 and time2 == True:  
                return render(request, 'level.html', {'player': player, 'level': level})

            if player.current_level >= 6:  
                return render(request, 'win.html', {'player': player})  
        

            #return render(request, 'level.html', {'player': player, 'level': level})
        except:
            if player.current_level > lastlevel:
                return render(request, 'win.html', {'player': player}) 
            return render(request, 'finish.html', {'player': player})
        '''
    elif ans=="":
        pass 
        # messages.error(request, "Please enter answer!")

    else :
        level.wrong = level.wrong + 1
        level.save()

        messages.error(request, "Wrong Answer!, Try Again")

    
    return render(request, 'finish.html', {'player': player})  


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
            'score':pl.score,
        })
        current_rank += 1
    #In order to allow non-dict objects to be serialized set the safe parameter to False
    return JsonResponse(players_list,safe=False)


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
        

class LevelList1(APIView):
    def get(self,request,format=None):
        Level=level.objects.all()
        serializer=levelSerializer1(Level,many=True)
        return Response(serializer.data)


class LevelList2(APIView):
    def get(self,request,format=None):
        Level=level2.objects.all()
        serializer=levelSerializer2(Level,many=True)
        return Response(serializer.data)


class LevelList3(APIView):
    def get(self,request,format=None):
        Level=level3.objects.all()
        serializer=levelSerializer3(Level,many=True)
        return Response(serializer.data)
