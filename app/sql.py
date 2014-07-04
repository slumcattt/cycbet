__author__ = 'Aiden'

from django.db import connection, transaction
from models import *
from django.contrib.auth.models import User, Group
import datetime, random

from bs4 import BeautifulSoup
import urllib

import bitcoinrpc as b
#c=b.connect_to_remote('aiden','Peyton18','107.170.92.113',8332)
conn = b.connect_to_remote('56a10cd1-a243-4c7e-9f6a-a7ad18c21ce1','keikolucky1','rpc.blockchain.info','80')
'''
set stage filter to where stage_status = 2 (not 1)
set stage statuses to 3 after payout
do payout logic
'''
base_url='http://www.procyclingstats.com'

def stageraces():
    race_page = urllib.urlopen('http://www.procyclingstats.com/races.php')
    rsoup = BeautifulSoup(race_page)
    table = rsoup.find("table")
    for row in table.findAll('tr')[1:]:
        str = "/"
        str2= "-"
        cols = row.findAll('td')
        startlist = cols[2].a.string
        race = latin1_to_ascii(cols[1].a.string) #un-euro the text
        nat = cols[1].img['src']
        nat = nat.split('/')[4].split('.')[0]
        cat = cols[3].string
        date = latin1_to_ascii(cols[0].string) #make date readable
        if '>>' in date:
            start_date = date.split('>>')[0]
            start_day = int(start_date.split('.')[0])
            start_month = int(start_date.split('.')[1])
            end_date = date.split('>>')[1]
            end_day = int(end_date.split('.')[0])
            end_month = int(end_date.split('.')[1])
            start_date = datetime.date(2014,start_month,start_day)
            end_date = datetime.date(2014,end_month,end_day)
            if startlist=='Startlist':
                raceObj = Race.objects.get_or_create(name=race,start_date=start_date,end_date=end_date,cat=cat,nat=nat)[0]
            else:
                pass #IGNORE PAST RACES
                #raceObj = Race.objects.get_or_create(name=race,start_date=start_date,end_date=end_date,cat=cat,nat=nat, status=3)[0]
        else:
            start_date = date
            day = int(date.split('.')[0])
            month = int(date.split('.')[1])
            date = datetime.date(2014,month,day)
            if startlist=='Startlist':
                raceObj = Race.objects.get_or_create(name=race,start_date=date,end_date=date,cat=cat,nat=nat)[0]
            else:
                pass #IGNORE PAST RACES
                #raceObj = Race.objects.get_or_create(name=race,start_date=date,end_date=date,cat=cat,nat=nat, status=3)[0]
        race_url = cols[1].a['href']
        seq = (base_url,race_url) # This is sequence of strings.
        full_race_url = str.join( seq )
        #GET STAGES FOR RACES
        if startlist=='Startlist':
            race_url = cols[1].a['href']
            seq = (base_url,race_url) # This is sequence of strings.
            full_race_url = str.join( seq )
            race_page = urllib.urlopen(full_race_url)
            racesoup = BeautifulSoup(race_page)
            seq2 = (full_race_url,'Stages') # This is sequence of strings.
            full_stages_url = str2.join( seq2 )
            stages_page = urllib.urlopen(full_stages_url)
            stagessoup = BeautifulSoup(stages_page)
            stable = stagessoup.find("table")
            for row in stable.findAll('tr')[1:]:
                cols2 = row.findAll('td')
                date = cols2[0].string
                day = int(date.split('.')[0])
                month = int(date.split('.')[1])
                date = datetime.date(2014,month,day)
                if cols2[2].a.string:
                    name = latin1_to_ascii(cols2[2].a.string)
                else:
                    name=raceObj.name
                distance = cols2[5].string
                stageObj = Stage.objects.get_or_create(name=name,race=raceObj,distance=distance,date=date)[0]
        else:
            pass #IGNORE OLD RACES
            '''
            race_url = cols[1].a['href']
            seq = (base_url,race_url) # This is sequence of strings.
            full_race_url = str.join( seq )
            race_page = urllib.urlopen(full_race_url)
            racesoup = BeautifulSoup(race_page)
            seq2 = (full_race_url,'Stages') # This is sequence of strings.
            full_stages_url = str2.join( seq2 )
            stages_page = urllib.urlopen(full_stages_url)
            stagessoup = BeautifulSoup(stages_page)
            stable = stagessoup.find("table")
            for row in stable.findAll('tr')[1:]:
                cols2 = row.findAll('td')
                date = cols2[0].string
                day = int(date.split('.')[0])
                month = int(date.split('.')[1])
                date = datetime.date(2014,month,day)
                if cols2[2].a.string:
                    name = latin1_to_ascii(cols2[2].a.string)
                else:
                    name=raceObj.name
                distance = cols2[5].string
                stageObj = Stage.objects.get_or_create(name=name,race=raceObj,distance=distance,date=date,status=3)[0]
            '''


def teams():
    team_page = urllib.urlopen('http://www.procyclingstats.com/teams/Teams-2014-WorldTour')
    tsoup = BeautifulSoup(team_page)
    for ta in tsoup.findAll('a', attrs={'class':'BlackToRed'}):
        team_name =  latin1_to_ascii(ta.string)
        #find a way to add that  fucking nationality
        teamObj= Team.objects.get_or_create(name=team_name)[0]
        team_url = ta['href']
        #print team_url
        str = '/'
        seq = (base_url,team_url) # This is sequence of strings.
        full_rider_url = str.join( seq )
        rider_page = urllib.urlopen(full_rider_url)
        rsoup = BeautifulSoup(rider_page)
        for a in rsoup.findAll('a'):
            if a.string:
                rider_name = latin1_to_ascii(a.string) if ',' in a.string else None
                if rider_name:
                    fname = rider_name.split(',')[0]
                    lname = rider_name.split(',')[1]
                    str3 = ''
                    seq3 = (fname,lname) # This is sequence of strings.
                    rider_name = str3.join( seq3 )
                    riderObj= Rider.objects.get_or_create(name=rider_name)[0]
                    riderObj.teams.add(teamObj)
    team_page = urllib.urlopen('http://www.procyclingstats.com/teams/Teams-2014-ProContinental')
    tsoup = BeautifulSoup(team_page)
    for ta in tsoup.findAll('a', attrs={'class':'BlackToRed'}):
        team_name =  latin1_to_ascii(ta.string)
        #find a way to add that  fucking nationality
        teamObj= Team.objects.get_or_create(name=team_name)[0]
        team_url = ta['href']
        #print team_url
        str = '/'
        seq = (base_url,team_url) # This is sequence of strings.
        full_rider_url = str.join( seq )
        rider_page = urllib.urlopen(full_rider_url)
        rsoup = BeautifulSoup(rider_page)
        for a in rsoup.findAll('a'):
            if a.string:
                rider_name = latin1_to_ascii(a.string) if ',' in a.string else None
                if rider_name:
                    fname = rider_name.split(',')[0]
                    lname = rider_name.split(',')[1]
                    str3 = ''
                    seq3 = (fname,lname) # This is sequence of strings.
                    rider_name = str3.join( seq3 )
                    riderObj= Rider.objects.get_or_create(name=rider_name)[0]
                    riderObj.teams.add(teamObj)

def racelist():
    race_page = urllib.urlopen('http://www.procyclingstats.com/races.php')
    rsoup = BeautifulSoup(race_page)
    table = rsoup.find("table")
    for row in table.findAll('tr')[1:]:
        str = "/"
        str2= "-"
        cols = row.findAll('td')
        startlist = cols[2].a.string
        '''
        race = latin1_to_ascii(cols[1].a.string) #un-euro the text
        raceObj=Race.objects.get_or_create(name=race)[0]
        '''
        if startlist=='Startlist':
            race = latin1_to_ascii(cols[1].a.string) #un-euro the text
            raceObj=Race.objects.get_or_create(name=race)[0]
            startlist_url = cols[2].a['href']
            seq = (base_url,startlist_url) # This is sequence of strings.
            full_startlist_url = str.join( seq )
            startlist_page = urllib.urlopen(full_startlist_url)
            startsoup = BeautifulSoup(startlist_page)
            for d in startsoup.findAll('div', style = 'width: 245px; float: left;  font: 12px/18px tahoma; '):
                for ta in d.findAll('a', attrs={'class':'BlackToRed'})[1:]:
                    rider =  latin1_to_ascii(ta.string)
                    db_riders=Rider.objects.all()
                    for dbr in db_riders:
                        rider_name = dbr.name
                        if rider == rider_name:
                            riderObj = Rider.objects.get(name=rider_name)
                            for s in Stage.objects.filter(race=raceObj):
                                stageRider = StageRider.objects.get_or_create(stage=s,rider=riderObj)


def doit():
    stageraces()
    teams()
    racelist()
    #fakeodds()

def payit():
    bet_pay()
    print 'Single bets paid and closed'
    parlay_pay()
    print 'Parlay bets run'


def bet_pay():
    #SET TODAYS STAGE TO PENDING (CANNOT BET ON ANYMORE)
    todays_stages=Stage.objects.filter(date=datetime.date.today())
    todays_stages.status=2
    #SELECT STAGES WHERE A WINNER IS MARKED OFF, PAYOUT SIGLE BETS ON THESE MARK PARLAY BETS AS
    offers=StageRider.objects.filter(stage__status=1)#Exclude open bets and closed - change to =2
    status_change_stage=None #For changing offers
    status_change_stages=[]
    for o in offers:
        betset=o.bet_set.filter(status=2) #get all submitted bets for a stage-rider
        for b in betset:
            status_change_stage,status_change_stages=make_bet_results(o,b,status_change_stage,status_change_stages)
    offers=StageRider.objects.filter(stage__status=1)
    for o in offers:
        if o.winres or o.gcres or o.mtnres or o.sprntres or o.ythres:
            #Following builds array of stages to close up because the result is recorded and you are paying
            if status_change_stage==o.stage:
                pass
            else:
                status_change_stage=o.stage
                status_change_stages.append(o.stage)
            settled_bets=o.bet_set.filter(status=2)
            #if there is a winner selected for a category, set all the bets to completed
            for sb in settled_bets:
                sb.status=3
                sb.save()
    for s in status_change_stages:
        s.status=3 #set the stage to completed wherever results were posted
        #s.save()
        print s

def make_bet_results(o,b,status_change_stage,status_change_stages):
    #if the offer has a result and it is a single bet
    if b.bet_cat=='STAGE' and o.winres and b.parlay==False:
        pay_amt=b.amt*b.odds
        b.res=True#PAYOUT HERE
        b.save()
        print b.amt, b.user, b.status
    if b.bet_cat=='GC' and o.gcres and b.parlay==False:
        pay_amt=b.amt*b.odds
        b.res=True#PAYOUT HERE
        b.save()
        print b.amt, b.user, b.status
    if b.bet_cat=='MTN' and o.mtnres and b.parlay==False:
        pay_amt=b.amt*b.odds
        b.res=True#PAYOUT HERE
        b.save()
        print b.amt, b.user, b.status
    if b.bet_cat=='SPRNT' and o.sprntres and b.parlay==False:
        pay_amt=b.amt*b.odds
        b.res=True#PAYOUT HERE
        b.save()
        print b.amt, b.user, b.status
    if b.bet_cat=='YTH' and o.ythres and b.parlay==False:
        pay_amt=b.amt*b.odds
        b.res=True#PAYOUT HERE
        b.save()
        print b.amt, b.user, b.status
    #if the offer has a result and it is a PARLAY
    if b.bet_cat=='STAGE' and o.winres and b.parlay==True:
        b.res=True
        b.save()
    if b.bet_cat=='GC' and o.gcres and b.parlay==True:
        b.res=True
        b.save()
    if b.bet_cat=='MTN' and o.mtnres and b.parlay==True:
        b.res=True
        b.save()
    if b.bet_cat=='SPRNT' and o.sprntres and b.parlay==True:
        b.res=True
        b.save()
    if b.bet_cat=='YTH' and o.ythres and b.parlay==True:
        b.res=True
        b.save()
    return status_change_stage,status_change_stages


def parlay_pay():
    open_parlays=Parlay.objects.filter(status=2)
    for op in open_parlays:
        pay=True
        winning_parlay_odds=[]
        open_parlay_bets=op.bet_set.all()
        for opb in open_parlay_bets:
            #if bet still open
            if opb.status !=3:
                pay=False
                print 'bet still open',op.id, opb.id
            #if won, append to winning bets string
            elif opb.res==True:
                winning_parlay_odds.append(opb.odds)
            else:
                #if closed or open and didn't win
                op.status=3
                op.save()
                pay=False
        if pay:
            tot_odds=1
            for wpo in winning_parlay_odds:
                tot_odds=tot_odds*wpo
            tot_amt=tot_odds*op.amt if op.amt else None
            op.status=3
            op.res=True
            op.save()
            #PAYOUT HERE
            print tot_amt,'PARLAY WIN'



'''
    BET_STATUS = (
        (1, 'Open'),
        (2, 'Pending'),
        (3, 'Completed'),
     )
'''
'''
def fakeodds():
    offers=StageRider.objects.filter(stage_id=72)
    for o in offers:
        w=random.randint(1, 20)
        g=random.randint(1, 20)
        s=random.randint(1, 20)
        m=random.randint(1, 20)
        y=random.randint(1, 20)
        o.winodds=w
        o.gcodds=g
        o.sprntodds=s
        o.mtnodds=m
        o.ythodds=y
        o.save()
'''

def latin1_to_ascii(unicrap_string):
    """This replaces UNICODE Latin-1 characters with
    something equivalent in 7-bit ASCII. All characters in the standard
    7-bit ASCII range are preserved. In the 8th bit range all the Latin-1
    accented letters are stripped of their accents. Most symbol characters
    are converted to something meaningful. Anything not converted is deleted.
    """
    xlate = {
        0xc0: 'A', 0xc1: 'A', 0xc2: 'A', 0xc3: 'A', 0xc4: 'A', 0xc5: 'A',
        0xc6: 'Ae', 0xc7: 'C',
        0xc8: 'E', 0xc9: 'E', 0xca: 'E', 0xcb: 'E',
        0xcc: 'I', 0xcd: 'I', 0xce: 'I', 0xcf: 'I',
        0xd0: 'Th', 0xd1: 'N',
        0xd2: 'O', 0xd3: 'O', 0xd4: 'O', 0xd5: 'O', 0xd6: 'O', 0xd8: 'O',
        0xd9: 'U', 0xda: 'U', 0xdb: 'U', 0xdc: 'U',
        0xdd: 'Y', 0xde: 'th', 0xdf: 'ss',
        0xe0: 'a', 0xe1: 'a', 0xe2: 'a', 0xe3: 'a', 0xe4: 'a', 0xe5: 'a',
        0xe6: 'ae', 0xe7: 'c',
        0xe8: 'e', 0xe9: 'e', 0xea: 'e', 0xeb: 'e',
        0xec: 'i', 0xed: 'i', 0xee: 'i', 0xef: 'i',
        0xf0: 'th', 0xf1: 'n',
        0xf2: 'o', 0xf3: 'o', 0xf4: 'o', 0xf5: 'o', 0xf6: 'o', 0xf8: 'o',
        0xf9: 'u', 0xfa: 'u', 0xfb: 'u', 0xfc: 'u',
        0xfd: 'y', 0xfe: 'th', 0xff: 'y',
        0xa1: '!', 0xa2: '{cent}', 0xa3: '{pound}', 0xa4: '{currency}',
        0xa5: '{yen}', 0xa6: '|', 0xa7: '{section}', 0xa8: '{umlaut}',
        0xa9: '{C}', 0xaa: '{^a}', 0xab: '<<', 0xac: '{not}',
        0xad: '-', 0xae: '{R}', 0xaf: '_', 0xb0: '{degrees}',
        0xb1: '{+/-}', 0xb2: '{^2}', 0xb3: '{^3}', 0xb4:"'",
        0xb5: '{micro}', 0xb6: '{paragraph}', 0xb7: '*', 0xb8: '{cedilla}',
        0xb9: '{^1}', 0xba: '{^o}', 0xbb: '>>',
        0xbc: '{1/4}', 0xbd: '{1/2}', 0xbe: '{3/4}', 0xbf: '?',
        0xd7: '*', 0xf7: '/'
    }
    r = ''
    for i in unicrap_string:
        if xlate.has_key(ord(i)):
            r += xlate[ord(i)]
        elif ord(i) >= 0x80:
            pass
        else:
            r += i
    return r


