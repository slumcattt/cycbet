from django.contrib import admin

# Register your models here.
from app.models import *


admin.site.register([Bet,StageTeam,StageRider,TeamImage,Team,RiderImage,Rider,RaceImage,Race,StageImage,Stage])

