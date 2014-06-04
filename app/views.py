from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
#from app.forms import *
from django.db import connection
from django.db.models import Max,Count, Min, Sum, Avg
#import json

from models import *
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout

from django.forms.models import modelformset_factory

# Create your views here.

import bitcoinrpc as b
c=b.connect_to_remote('aiden','Peyton18','107.170.92.113',8332)

def index(request):
    msg='nothing'
    if request.method == 'POST':
        msg=c.getbalance()
    context={'msg': msg}
    return render(request, 'app/index.html',context)

def logout_view(request):
    logout(request)
    return redirect('app.views.index')