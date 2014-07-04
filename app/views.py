from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
from app.forms import *
from django.db import connection
from django.db.models import Max,Count, Min, Sum, Avg
import json

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
conn = b.connect_to_remote('56a10cd1-a243-4c7e-9f6a-a7ad18c21ce1','keikolucky1','rpc.blockchain.info','80')
#conn = b.connect_to_local()


races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))


def ab(user):
    account=str(user)
    account_balance=1000*float(conn.getbalance(account))
    return account, account_balance
    #return 'aiden',2000

def index(request):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5)).exclude(name='General Classification')
    if request.user.is_authenticated():
        account,account_balance=ab(request.user)
        parlay = Parlay(user=request.user, status=1)
        pform=Parlays(instance=parlay)
        (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
        if request.method == 'POST':
            pform = Parlays(request.POST)
            bet_data = BetFormset(request.POST, prefix='bet')
            if bet_data.is_valid() and pform.is_valid():
                parlay = pform.save(commit=False)
                parlay.status=2
                parlay.save()
                save_parlay=False
                tot_amt=parlay.amt
                for form in bet_data.cleaned_data:
                    if (form['amt'] > 0 and form['parlay']==False) or (form['parlay'] and parlay.amt>0):
                        form['id'].status = 2
                        form['id'].amt = form['amt']
                        form['id'].parlay = form['parlay']
                        if form['parlay'] and parlay.amt>0:
                            form['id'].parlay_bet = parlay
                            save_parlay=True
                        form['id'].save()
                if not save_parlay:
                    parlay.delete()
                (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
    return render(request, 'app/index.html',locals())

def race(request, race_id=None):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    race=None
    stages=None
    if Race.objects.get(id=race_id).status==1:
        race=Race.objects.get(id=race_id)
        stages=Stage.objects.filter(race_id=race_id,date__gt=datetime.date.today()).exclude(name__in=['General Classification',race.name])
        overall = Stage.objects.get(race=race,name='General Classification') if Stage.objects.filter(race=race,name='General Classification').count()>0 else Stage.objects.get(race=race)
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
            account,account_balance=ab(request.user)
            parlay = Parlay(user=request.user, status=1)
            pform=Parlays(instance=parlay)
            (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
            if request.method == 'POST':
                pform = Parlays(request.POST)
                bet_data = BetFormset(request.POST, prefix='bet')
                if bet_data.is_valid() and pform.is_valid():
                    parlay = pform.save(commit=False)
                    parlay.status=2
                    parlay.save()
                    print parlay.id
                    save_parlay=False
                    tot_amt=parlay.amt
                    for form in bet_data.cleaned_data:
                        print form['id'].odds
                        if (form['amt'] > 0 and form['parlay']==False) or (form['parlay'] and parlay.amt>0):
                            form['id'].status = 2
                            form['id'].amt = form['amt']
                            form['id'].parlay = form['parlay']
                            if form['parlay'] and parlay.amt>0:
                                form['id'].parlay_bet = parlay
                                save_parlay=True
                            form['id'].save()
                    if not save_parlay:
                        parlay.delete()
                    (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
    else:
        return redirect('app.views.index')#make a custom 404 for this- bet over
    return render(request, 'app/race.html', locals())

def stage(request, stage_id=None):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    race=None
    stage=None
    stages=None
    stage_riders=None
    if Stage.objects.get(id=stage_id).status==1 and Stage.objects.get(id=stage_id).name!='General Classification':
        stage=Stage.objects.get(id=stage_id)
        race=stage.race
        stages=Stage.objects.filter(race_id=race.id,date__gt=datetime.date.today()).exclude(name__in=['General Classification',race.name])
        stage_riders=StageRider.objects.filter(stage=stage, winodds__gt=0)
        odds_formset = OddsFormset(queryset=stage_riders)
        for b in range(len(odds_formset)):
            odds_formset[b].lbl = stage_riders[b]
            odds_formset[b].team = stage_riders[b].rider.teams.all()[0]
            odds_formset[b].oddslabel = stage_riders[b].winodds
        if request.user.is_authenticated():
            account,account_balance=ab(request.user)
            parlay = Parlay(user=request.user, status=1)
            pform=Parlays(instance=parlay)
            (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
            if request.method == 'POST':
                pform = Parlays(request.POST)
                bet_data = BetFormset(request.POST, prefix='bet')
                if bet_data.is_valid() and pform.is_valid():
                    parlay = pform.save(commit=False)
                    parlay.status=2
                    parlay.save()
                    save_parlay=False
                    tot_amt=parlay.amt
                    for form in bet_data.cleaned_data:
                        if (form['amt'] > 0 and form['parlay']==False) or (form['parlay'] and parlay.amt>0):
                            form['id'].status = 2
                            form['id'].amt = form['amt']
                            form['id'].parlay = form['parlay']
                            if form['parlay'] and parlay.amt>0:
                                form['id'].parlay_bet = parlay
                                save_parlay=True
                            form['id'].save()
                    if not save_parlay:
                        parlay.delete()
                    (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
    else:
        return redirect('app.views.index')#make a custom 404 for this- bet over
    return render(request, 'app/stage.html',locals())

#@csrf_exempt
def add_to_betslip(request):
    off_id_str=request.POST['off_id']
    off_id = off_id_str.split('_')[0]
    gc_or_other=off_id_str.split('_')[1]
    offer=StageRider.objects.get(id=int(off_id))
    if gc_or_other == 'STAGE':
        bet_object=Bet.objects.create(offer=offer,user=request.user,bet_cat=gc_or_other, odds = offer.winodds)
    if gc_or_other == 'GC':
        bet_object=Bet.objects.create(offer=offer,user=request.user,bet_cat=gc_or_other, odds = offer.gcodds)
    if gc_or_other == 'MTN':
       bet_object=Bet.objects.create(offer=offer,user=request.user,bet_cat=gc_or_other, odds = offer.mtnodds)
    if gc_or_other == 'SPRNT':
        bet_object=Bet.objects.create(offer=offer,user=request.user,bet_cat=gc_or_other, odds = offer.sprntodds)
    if gc_or_other == 'YTH':
        bet_object=Bet.objects.create(offer=offer,user=request.user,bet_cat=gc_or_other, odds = offer.ythodds)
    (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
    data = t.render(c)
    return HttpResponse(data)

#@csrf_exempt
def remove_from_betslip(request):
    bet_id=request.POST['bet_id']
    b=Bet.objects.get(id=bet_id)
    b.delete()
    (bet_formset, bet_queryset, t, c) = make_bet_table(request.user)
    data = t.render(c)
    return HttpResponse(data)


def make_bet_table(user):
    open_bets = Bet.objects.filter(status=1, user=user)
    formset = BetFormset(queryset=open_bets, prefix='bet')
    t=Template("{{formset.management_form}}{% for tr in formset%}<tr id='{{tr.lbl.id}}'> <td>{{tr.id}}{{tr.odds}}{{tr.offer}}{{tr.user}}{{tr.status}}{{tr.bet_cat}} <b>{{ tr.rider}} - <small>{{tr.team}}</small></b><br><small>{{tr.stage}}-{{tr.comp}}</small></td><td>{{tr.oddslabel}}:1</td> <td><div id='amt-{{tr.lbl.id}}'>{{tr.amt}}</div></td><td>{{tr.parlay}}</td><td><img src='/static/img/x.png' class='small remove_bet'></td></tr>{%endfor%}")
    c = Context({"formset":formset})
    for b in range(len(formset)):
        formset[b].lbl = open_bets[b]
        formset[b].rider = open_bets[b].offer.rider
        if open_bets[b].bet_cat == 'STAGE':
            formset[b].oddslabel = open_bets[b].offer.winodds
            formset[b].comp = open_bets[b].bet_cat
        if open_bets[b].bet_cat == 'GC':
            formset[b].oddslabel = open_bets[b].offer.gcodds
            formset[b].comp = open_bets[b].bet_cat
        if open_bets[b].bet_cat == 'MTN':
            formset[b].oddslabel = open_bets[b].offer.mtnodds
            formset[b].comp = open_bets[b].bet_cat
        if open_bets[b].bet_cat == 'SPRNT':
            formset[b].oddslabel = open_bets[b].offer.sprntodds
            formset[b].comp = open_bets[b].bet_cat
        if open_bets[b].bet_cat == 'YTH':
            formset[b].oddslabel = open_bets[b].offer.ythodds
            formset[b].comp = open_bets[b].bet_cat
        formset[b].stage = open_bets[b].offer.stage
        formset[b].race = open_bets[b].offer.stage.race
        formset[b].team = open_bets[b].offer.rider.teams.all()[0]
    return (formset, open_bets, t, c)


def logout_view(request):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    ustages = Stage.objects.filter(status=1,date__lt=datetime.date.today() + timedelta(days=5))
    if request.user.is_authenticated():
        a=1
    logout(request)
    return redirect('app.views.index',locals())

def register(request, *args, **kwargs):
    reg_form = UserCreateForm(request.POST)
    if reg_form.is_valid():
        username = reg_form.clean_username()
        password = reg_form.clean_password2()
        reg_form.save()
        user = authenticate(username=username,
                            password=password)
        login(request, user)
        conn.getnewaddress(username)
        return redirect('app.views.index')
    return render(request, 'app/register.html',locals())

def account(request):
    races=Race.objects.filter(status=1,start_date__lt=datetime.date.today() + timedelta(days=30))
    account,account_balance=ab(request.user)
    account_address=conn.getaddressesbyaccount(account)
    if request.user.is_authenticated():
        #----
        account_open_single_bets=Bet.objects.filter(user=request.user, status=2, parlay=False)
        account_open_single_bets =account_bets(account_open_single_bets)
        #----
        account_open_parlay_bets=Parlay.objects.filter(user=request.user, status=2)
        account_open_parlay_bets=account_parlays(account_open_parlay_bets)
        #-----
        account_closed_single_bets=Bet.objects.filter(user=request.user, status=3, parlay=False)
        account_closed_single_bets =account_bets(account_closed_single_bets)
        #-----
        account_closed_parlay_bets=Parlay.objects.filter(user=request.user, status=3)
        account_closed_parlay_bets =account_parlays(account_closed_parlay_bets)
    return render(request, 'app/account.html', locals())

def account_bets(queryset):
    for b in queryset:
        b.team = b.offer.rider.teams.all()[0]
        seq=(b.offer.rider.name,b.offer.stage.name,b.offer.stage.race.name,b.bet_cat)
        b.bet_string='-'.join(seq)
    return queryset

def account_parlays(queryset):
    '''
    class, parlay id, , , ,amt
    class,rider-race-stage-categ,odds
    '''
    col_par_tbl=[]
    for p in queryset:
        pod=1
        res=False
        child_rows=[]
        for b in p.bet_set.all():
            cl='child'
            seq=(b.offer.rider.name,b.offer.stage.name,b.offer.stage.race.name,b.bet_cat)
            be='-'.join(seq)
            '''
            if b.bet_cat == 'STAGE':
                b.odds = b.offer.winodds
                b.res = b.offer.winres
            if b.bet_cat == 'GC':
                b.odds = b.offer.gcodds
                b.res = b.offer.gcres
            if b.bet_cat == 'MTN':
                b.odds = b.offer.mtnodds
                b.res = b.offer.mtnres
            if b.bet_cat == 'SPRNT':
                b.odds = b.offer.sprntodds
                b.res = b.offer.sprntres
            if b.bet_cat == 'YTH':
                b.odds = b.offer.ythodds
                b.res = b.offer.ythres
            '''
            pod=pod*b.odds
            child_rows.append(['child', be, b.odds,'-',b.res])
        col_par_tbl.append(['header', 'Parlay # %i'%p.id,pod, p.amt,p.res])
        col_par_tbl+=child_rows
    print col_par_tbl
    return col_par_tbl


def get_new_address(request):
    account=str(request.user)
    new_add=conn.getnewaddress(account)
    return redirect('app.views.account')


def withdraw(request):
    account=str(request.user)
    to_address=str(request.POST['to_address'])
    amt=float(request.POST['amt'])/1000
    cmt=request.POST['to_address']
    conn.sendfrom(account,to_address, amt,1,cmt)
    return redirect('app.views.account')


def delete_acct(request):
    account=str(request.user)
    return redirect('app.views.account')


def set_odds(request,stage_id=None):
    stage = None
    rider_formset = None
    if stage_id:
        stage = Stage.objects.get(pk=stage_id)
        rider_queryset = StageRider.objects.filter(stage_id=stage_id)
        rider_formset = OddsFormSet(queryset=rider_queryset)
        for r in range(rider_queryset.count()):
            rider_formset[r].visit = rider_queryset[r]
    snav = StageDropdown()
    return render(request, 'app/set_odds.html', locals())


