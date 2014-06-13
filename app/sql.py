__author__ = 'Aiden'

from django.db import connection, transaction
from models import *
from django.contrib.auth.models import User, Group
import datetime, random

from bs4 import BeautifulSoup
import urllib
'''
for race
open startlist soup
for r in rider=
RiderStage(rider=r, stage=s
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
                raceObj = Race.objects.get_or_create(name=race,start_date=start_date,end_date=end_date,cat=cat,nat=nat, status=3)[0]
        else:
            start_date = date
            day = int(date.split('.')[0])
            month = int(date.split('.')[1])
            date = datetime.date(2014,month,day)
            if startlist=='Startlist':
                raceObj = Race.objects.get_or_create(name=race,start_date=date,end_date=date,cat=cat,nat=nat)[0]
            else:
                raceObj = Race.objects.get_or_create(name=race,start_date=date,end_date=date,cat=cat,nat=nat, status=3)[0]
        race_url = cols[1].a['href']
        seq = (base_url,race_url) # This is sequence of strings.
        full_race_url = str.join( seq )
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
        race = latin1_to_ascii(cols[1].a.string) #un-euro the text
        raceObj=Race.objects.get_or_create(name=race)[0]
        if startlist=='Startlist':
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

#Yeah, don't do this
def delete_gc_stages():
    stages = Stage.objects.filter(name='General Classification')
    for s in stages:
        riders = StageRider.objects.filter(stage=s)
        for r in riders:
            bets=Bet.objects.filter(offer=r)
            for b in bets:
                b.delete()
            r.delete()
        s.delete()


def doit():
    stageraces()
    teams()
    racelist()





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


'''
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def fake_data():
    mkpjstskslstnrs()
    #RELATING TABLES==============================================================================================
    #MANY TO MANY the Projects and Tasks through ProjectTask table
    projtasks()
    #MANY TO MANY (no thru table) listeners - visits, projects - visits
    many2many()

def mkpjstskslstnrs():
    p1=Project.objects.get_or_create(name='First Project',leader_id=User.objects.get(id=1).id,deadline=datetime.date.today(),overall_priority=2)
    p2=Project.objects.get_or_create(name='Second Project',leader_id=User.objects.get(id=1).id,deadline=datetime.date.today(),overall_priority=3)
    p3=Project.objects.get_or_create(name='Third Project',leader_id=User.objects.get(id=1).id,deadline=datetime.date(2012,02,01),overall_priority=2)
    p4=Project.objects.get_or_create(name='Fourth Project',leader_id=User.objects.get(id=1).id,deadline=datetime.date(2029,02,01),overall_priority=4)
    p1.save()
    p2.save()
    p3.save()
    p4.save()
    #Create Various Tasks===========
    t1=Task.objects.get_or_create(name='Play')
    t2=Task.objects.get_or_create(name='Talk')
    t3=Task.objects.get_or_create(name='Sleep')
    t4=Task.objects.get_or_create(name='Lunch')
    t1.save()
    t2.save()
    t3.save()
    t4.save()
    name_list=['Tom','Mary','SharkBoy','ManateeMan','-___-']
    for i in name_list:
        #Yeah, this S1, S2 stuff doesn't do what I thought but whatever
        sr=random.randint(1, 2)
        rr=random.randint(1, 6)
        er=random.randint(1, 2)
        sx='S'+str(sr)
        et='E'+str(rr)
        ra='R'+str(er)
        l = Listener(name=i,race=ra,eth=et,sex=sx,visit=Visit.objects.get(id=random.randint(1, 60)))
        l.save()

def projtasks():
    for i in Project.objects.all():
        for j in Task.objects.all():
            pri=random.randint(1,4)
            pt=ProjectTask(project=i, task=j, priority=pri)
            pt.save()

def many2many():
    pjs=Project.objects.all()
    for pj in pjs:
        r1=random.randint(1,200)
        r2=random.randint(1,200)
        pj.visits.add(Visit.objects.get(id=r1),Visit.objects.get(id=r2))
        pj.save()
'''