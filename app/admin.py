from django.contrib import admin

# Register your models here.
from app.models import *


admin.site.register([Category,Match,Image,Offer,Bet,Parlay])