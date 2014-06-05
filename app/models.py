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
    name = models.CharField(max_length=200, default='Overall')
    race = models.ForeignKey('Race', null=True, blank=True)
    stage = models.IntegerField(max_length=3, null=True, blank=True) #0= GC
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    rider = models.ManyToManyField('Rider',through='StageRider')
    team = models.ManyToManyField('Team',through='StageTeam')
    status = models.IntegerField(max_length=3, null=True, blank=True, choices=BET_STATUS)
    def __str__(self):
        return self.name

class StageImage(models.Model):
    img = models.ImageField(upload_to='stage',null=True)
    race = models.ForeignKey('Stage')

class Race(models.Model):
    NAT_CHOICES = (
        ('US', 'USA'),
        ('UK', 'United Kingdom'),
        ('IT', 'Italy'),
     )
    name = models.CharField(max_length=200)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    nat = models.CharField(max_length=50, null=True, blank=True, choices=NAT_CHOICES)
    def __str__(self):
        return self.name

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
    dob = models.DateTimeField(verbose_name='DOB', null=True, blank=True)
    team = models.ManyToManyField('Team')
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
    bets = models.ManyToManyField('Bet')

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

class Bet(models.Model):
      amt = models.FloatField(null=True, blank=True,verbose_name="bet amount mBtC")
      user = models.ForeignKey(User)
      paid=models.NullBooleanField(default=False)
      parlay=models.BooleanField(null=False, blank=False, default=False)