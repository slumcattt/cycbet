from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from app.forms import *
from django.db import connection
from django.db.models import Max,Count, Min, Sum, Avg
#import json

from models import *
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout


from django.template import  Template, Context

from django.forms.models import modelformset_factory
OddsFormset = modelformset_factory(StageRider, form=Odds, extra=0, max_num=1)
BetFormset = modelformset_factory(Bet, form=Bets, extra=0, max_num=1)

from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User

#logic not great in make_new_bet, add ajaxfix, remove the csrf exempt, post for submit bet, payout logic, closing bet logic, register, bitcoin stuff

from datetime import timedelta
import datetime
# Create your views here.

import bitcoinrpc as b
#c=b.connect_to_remote('aiden','Peyton18','107.170.92.113',8332)
conn=b.connect_to_remote('56a10cd1-a243-4c7e-9f6a-a7ad18c21ce1','keikolucky1','rpc.blockchain.info','80')


races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))


def index(request):
    account_balance=2
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    if request.user.is_authenticated():
        logged_in=True
        (bet_formset, bet_queryset) = make_bet_table(request.user)
        if request.method == 'POST':
            msg=c.getnewaddress()
    else:
        logged_in=False
    context={'races': races,'ustages':ustages}
    return render(request, 'app/index.html',locals())

def race(request, race_id=None):
    account_balance=2
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    race=None
    stages=None
    if race_id:
        race=Race.objects.get(id=race_id)
        stages=Stage.objects.filter(race_id=race_id)
        overall = Stage.objects.get(race=race,name='General Classification')
        gc_riders=StageRider.objects.filter(stage=overall,gcodds__gt=0)
        for s in range(len(gc_riders)):
            gc_riders[s].team = gc_riders[s].rider.teams.all()[0]
        mtn_riders=StageRider.objects.filter(stage=overall,mtnodds__gt=0)
        for s in range(len(mtn_riders)):
            mtn_riders[s].team = mtn_riders[s].rider.teams.all()[0]
        sprnt_riders=StageRider.objects.filter(stage=overall,sprntodds__gt=0)
        for s in range(len(sprnt_riders)):
            sprnt_riders[s].team = sprnt_riders[s].rider.teams.all()[0]
        yth_riders=StageRider.objects.filter(stage=overall,ythodds__gt=0)
        for s in range(len(yth_riders)):
            yth_riders[s].team = yth_riders[s].rider.teams.all()[0]
        if request.user.is_authenticated():
            logged_in=True
            (bet_formset, bet_queryset) = make_bet_table(request.user)
            if request.method == 'POST':
                print 'posterized'
        else:
            logged_in=False
    return render(request, 'app/race.html', locals())

def stage(request, stage_id=None):
    account_balance=2
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    race=None
    stage=None
    stages=None
    stage_riders=None
    if stage_id:
        stage=Stage.objects.get(id=stage_id)
        race=stage.race
        stages=Stage.objects.filter(race_id=race.id)
        stage_riders=StageRider.objects.filter(stage=stage, winodds__gt=0)
        odds_formset = OddsFormset(queryset=stage_riders)
        for b in range(len(odds_formset)):
            odds_formset[b].lbl = stage_riders[b]
            odds_formset[b].team = stage_riders[b].rider.teams.all()[0]
            odds_formset[b].odds = stage_riders[b].winodds
        if request.user.is_authenticated():
            logged_in=True
            (bet_formset, bet_queryset) = make_bet_table(request.user)
            if request.method == 'POST':
                parlay_amt=request.POST['parlay_amt']
                print parlay_amt
                bet_data = BetFormset(request.POST, prefix='bet')
                if bet_data.is_valid():
                    for form in bet_data.cleaned_data:  #I ALSO TESETED formset.forms
                        form['status']=2
                        print (form['bet_cat'], form['status'])
                    bet_data.save()
        else:
            logged_in=False
    return render(request, 'app/stage.html',locals())

#@csrf_exempt
def add_to_betslip(request):
    off_id_str=request.POST['off_id']
    off_id = off_id_str.split('_')[0]
    gc_or_other=off_id_str.split('_')[1]
    offer=StageRider.objects.get(id=int(off_id))
    (t,c)=make_new_bet(request.user, offer, gc_or_other)
    return HttpResponse(t.render(c))
    #return redirect('app.views.index')

#@csrf_exempt
def remove_from_betslip(request):
    bet_id=request.POST['bet_id']
    b=Bet.objects.get(id=bet_id)
    b.delete()
    return HttpResponse('')


def make_bet_table(user):
    queryset = Bet.objects.filter(status=1, user=user)
    formset = BetFormset(queryset=queryset, prefix='bet')
    for b in range(len(formset)):
        formset[b].lbl = queryset[b]
        formset[b].rider = queryset[b].offer.rider
        if queryset[b].bet_cat == 'STAGE':
            formset[b].odds = queryset[b].offer.winodds
            formset[b].comp = queryset[b].bet_cat
        if queryset[b].bet_cat == 'GC':
            formset[b].odds = queryset[b].offer.gcodds
            formset[b].comp = queryset[b].bet_cat
        if queryset[b].bet_cat == 'MTN':
            formset[b].odds = queryset[b].offer.mtnodds
            formset[b].comp = queryset[b].bet_cat
        if queryset[b].bet_cat == 'SPRNT':
            formset[b].odds = queryset[b].offer.sprntodds
            formset[b].comp = queryset[b].bet_cat
        if queryset[b].bet_cat == 'YTH':
            formset[b].odds = queryset[b].offer.ythodds
            formset[b].comp = queryset[b].bet_cat
        formset[b].stage = queryset[b].offer.stage
        formset[b].race = queryset[b].offer.stage.race
        formset[b].team = queryset[b].offer.rider.teams.all()[0]
    return (formset, queryset)

def make_new_bet(user, offer, gc_or_other):
    open_bets = Bet.objects.filter(status=1, user=user)
    bet_object=Bet.objects.create(user=user,offer=offer,bet_cat=gc_or_other)
    for b in open_bets:
        #logic not great
        if (b.bet_cat == bet_object.bet_cat) and (b.offer.stage == bet_object.offer.stage) and (b.offer.rider != bet_object.offer.rider):
            t=Template("")
            c = Context({"new_bet":None})
            bet_object.delete()
            return (t,c)
        else:
            open_bets = Bet.objects.filter(status=1, user=user)
            formset = BetFormset(queryset=open_bets, prefix='bet')
            t=Template("<tr id='{{new_bet.lbl.id}}'> <td>{{new_bet.id}}{{new_bet.offer}}{{new_bet.user}}{{new_bet.status}} <b>{{ new_bet.rider}} - <small>{{new_bet.team}}</small></b><br><small>{{new_bet.stage}}-{{new_bet.comp}}</small></td><td>{{new_bet.odds}}:1</td> <td><div id='amt-{{new_bet.lbl.id}}'>{{new_bet.amt}}</div></td><td>{{new_bet.parlay}}</td><td><img src='/static/img/x.png' class='small remove_bet'></td></tr>")
            form_row = formset[len(formset)-1]
            form_row.lbl = bet_object
            form_row.rider = bet_object.offer.rider
            if bet_object.bet_cat == 'STAGE':
                form_row.odds = bet_object.offer.winodds
                form_row.comp = bet_object.bet_cat
            if bet_object.bet_cat == 'GC':
                form_row.odds = bet_object.offer.gcodds
                form_row.comp = bet_object.bet_cat
            if bet_object.bet_cat == 'MTN':
                form_row.odds = bet_object.offer.mtnodds
                form_row.comp = bet_object.bet_cat
            if bet_object.bet_cat == 'SPRNT':
                form_row.odds = bet_object.offer.sprntodds
                form_row.comp = bet_object.bet_cat
            if bet_object.bet_cat == 'YTH':
                form_row.odds = bet_object.offer.ythodds
                form_row.comp = bet_object.bet_cat
            form_row.stage = bet_object.offer.stage
            form_row.race = bet_object.offer.stage.race
            form_row.team = bet_object.offer.rider.teams.all()[0]
            c = Context({"new_bet":form_row})
            return (t,c)

def account(request):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    if request.user.is_authenticated():
        logged_in=True
    else:
        logged_in=False
    return render(request, 'app/account.html',locals())

def logout_view(request):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    if request.user.is_authenticated():
        logged_in=True
    else:
        logged_in=False
    logout(request)
    return redirect('app.views.index',locals())