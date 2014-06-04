from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse
#from app.forms import *
from django.db import connection
from django.db.models import Max,Count, Min, Sum, Avg
#import json

from models import *
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
#Model formsets for 'table forms' - forms in the tables for all the visit sub-tasks

from django.forms.models import modelformset_factory

# Create your views here.

import bitcoinrpc as b
c=b.connect_to_remote('aiden','Peyton18','107.170.92.113', port='8333')

def index(request):
    msg='nothing'
    if request.method == 'POST':
        msg=c.getbalance()
    context={'msg': msg}
    return render(request, 'app/index.html',context)