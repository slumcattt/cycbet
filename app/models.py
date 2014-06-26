from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class Stage(models.Model):
    BET_STATUS = (
        (1, 'Open'),
        (2, 'Pending'),
        (3, 'Completed'),
     )
    name = models.CharField(max_length=200, null=True, blank=True)
    race = models.ForeignKey('Race', null=True, blank=True)
    distance = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) #0= GC
    date = models.DateField(verbose_name='Date', null=True, blank=True)
    rider = models.ManyToManyField('Rider',through='StageRider')
    #team = models.ManyToManyField('Team',through='StageTeam')
    status = models.IntegerField(max_length=3, null=True, blank=True, choices=BET_STATUS, default=1)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['date']

class StageImage(models.Model):
    img = models.ImageField(upload_to='stage',null=True)
    race = models.ForeignKey('Stage')

class Race(models.Model):
    NAT_CHOICES = (
        ('au','Australia'),
        ('be','Belgium'),
        ('ca','Canada'),
        ('ch','Switzerland'),
        ('cn','China'),
        ('de','Germany'),
        ('es','Spain'),
        ('fr','France'),
        ('it','Italy'),
        ('ng','Norway'),
        ('nl','Netherlands'),
        ('pl','Poland'),
        ('uk','United Kingdom'),
        ('us','USA'),
     )
    BET_STATUS = (
        (1, 'Open'),
        (2, 'Pending'),
        (3, 'Completed'),
     )
    name = models.CharField(max_length=200)
    start_date = models.DateField(verbose_name='Start Date', null=True, blank=True)
    end_date = models.DateField(verbose_name='End Date', null=True, blank=True)
    nat = models.CharField(max_length=50, null=True, blank=True, choices=NAT_CHOICES)
    cat = models.CharField(max_length=50, null=True, blank=True)
    status = models.IntegerField(max_length=3, null=True, blank=True, choices=BET_STATUS, default=1)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['start_date']

class RaceImage(models.Model):
    img = models.ImageField(upload_to='race',null=True)
    race = models.ForeignKey('Race')

class Rider(models.Model):
    NAT_CHOICES = (
        ('US', 'USA'),
        ('UK', 'United Kingdom'),
        ('IT', 'Italy'),
     )
    name = models.CharField(max_length=200)
    dob = models.DateField(verbose_name='DOB', null=True, blank=True)
    teams = models.ManyToManyField('Team')
    nat = models.CharField(max_length=50, null=True, blank=True, choices=NAT_CHOICES)
    def __str__(self):
        return self.name

class RiderImage(models.Model):
    img = models.ImageField(upload_to='rider',null=True)
    race = models.ForeignKey('Rider')

class Team(models.Model):
    NAT_CHOICES = (
        ('US', 'USA'),
        ('UK', 'United Kingdom'),
        ('IT', 'Italy'),
     )
    name = models.CharField(max_length=200)
    nat = models.CharField(max_length=50, null=True, blank=True, choices=NAT_CHOICES)
    def __str__(self):
        return self.name

class TeamImage(models.Model):
    img = models.ImageField(upload_to='team',null=True)
    race = models.ForeignKey('Team')

class StageRider(models.Model):
    RES_CHOICES = (
        (True, 'W'),
        (False, 'L'),
     )
    stage = models.ForeignKey('Stage')
    rider = models.ForeignKey('Rider')
    winodds = models.IntegerField(max_length=5, null=True, blank=True)
    gcodds = models.IntegerField(max_length=5, null=True, blank=True)
    mtnodds = models.IntegerField(max_length=5, null=True, blank=True)
    sprntodds = models.IntegerField(max_length=5, null=True, blank=True)
    ythodds = models.IntegerField(max_length=5, null=True, blank=True)
    winres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    gcres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    mtnres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    sprntres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    ythres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    #bets = models.ManyToManyField('Bet',null=True,blank=True)
    def __str__(self):
        return ','.join([self.stage.race.name, self.stage.name, self.rider.name])
    class Meta:
        ordering = ['stage']
'''
class StageTeam(models.Model):
    RES_CHOICES = (
        (True, 'W'),
        (False, 'L'),
     )
    stage = models.ForeignKey('Stage')
    team = models.ForeignKey('Team')
    winodds = models.IntegerField(max_length=5, null=True, blank=True)
    winres = models.BooleanField(null=False, blank=True, choices=RES_CHOICES, default=False)
    bets = models.ManyToManyField('Bet')
'''

class Bet(models.Model):
    BET_STATUS = (
        (1, 'Open'),
        (2, 'Submitted'),
        (3, 'Paid'),
     )
    BET_CATS = (
        ('STAGE', 'Stage Winner'),
        ('GC', 'General Classification'),
        ('MTN', 'King of the Mountains'),
        ('SPRNT', 'Sprinter'),
        ('YTH', 'Youth'),
     )
    amt = models.FloatField(null=True, blank=True,verbose_name="bet amount mBtC")
    user = models.ForeignKey(User)
    offer = models.ForeignKey("StageRider")
    status=models.IntegerField(max_length=1,choices=BET_STATUS,default=1)
    parlay=models.BooleanField(null=False, blank=False, default=False)
    parlay_bet=models.ForeignKey("Parlay", null=True, blank=True)
    bet_cat = models.CharField(null=False, max_length=10,blank = False, choices = BET_CATS)
    class Meta:
        unique_together = ("user","status","offer","bet_cat","parlay_bet")
        ordering = ['id']

class Parlay(models.Model):
    BET_STATUS = (
        (1, 'Open'),
        (2, 'Submitted'),
        (3, 'Paid'),
     )
    amt = models.FloatField(null=True, blank=True,verbose_name="Parlay Amount mBtC")
    user = models.ForeignKey(User)
    status=models.IntegerField(max_length=1,choices=BET_STATUS,default=1)
    class Meta:
        #unique_together = ("user","status")
        ordering = ['id']