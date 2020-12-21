from django.shortcuts import render
from django.http import HttpResponse
import json
from server.models import *
from django.core import serializers
from collections import OrderedDict

# Create your views here.



def testing(request):


    r = Routine(name='Welding 0')
    r.save()
    print(r.id)
    #
    # rp = RobotProfile(name='UR Cobot', points={'x':2.0,'y':4.0,'z':8.0} ,routine = r)
    # rp.save()
    # print('forign key: ', rp.routine.id)
    # print('primary key: ', rp.id)

    # data = json.loads(serializers.serialize('json', RobotProfile.objects.all()))
    # print(type(data))
    # print(data)
    # origionaldata = data[0]["fields"]
    # print(type(origionaldata))
    # print(origionaldata)
    # pointsList = origionaldata["points"]
    # print(type(pointsList))
    # print(pointsList)
    #
    # dct = dict(eval(pointsList))
    # print(dct)

    # serializers.serialize('json', RobotProfile.objects.all())

    return HttpResponse(serializers.serialize('json', Routine.objects.all()))