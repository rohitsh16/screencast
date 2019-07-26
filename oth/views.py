from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import models
from django.contrib import messages
from oth import models
import datetime

def landing(request):
    return render(request, 'landing.html')

def index(request):

    m_level = models.total_level.objects.get(id=1)
    lastlevel = m_level.totallevel

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
    
    m_level = models.total_level.objects.get(id=1)
    lastlevel = m_level.totallevel
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
