import argparse
import socket
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import response, decorators, permissions, status
import json
import random
from django.core import serializers
from PoseDetection import PoseEstimation
from collections import OrderedDict

# parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
#
# parser.add_argument('--resize', type=str, default='0x0',
#                     help='if provided, resize images before they are processed. default=0x0, Recommends : 432x368 or 656x368 or 1312x736 ')
# parser.add_argument('--resize-out-ratio', type=float, default=4.0,
#                     help='if provided, resize heatmaps before they are post-processed. default=1.0')
#
# parser.add_argument('--model', type=str, default='cmu',
#                     help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
# parser.add_argument('--show-process', type=bool, default=False,
#                     help='for debug purpose, if enabled, speed for inference is dropped.')
# parser.add_argument('--option', type=str, default="camera", help="Camera / Kinect / image_path / camera_image")
# parser.add_argument('--tensorrt', type=str, default="False",
#                     help='for tensorrt process.')
# args = parser.parse_args()

# from server.models import RobotProfile, Points
from server.models import *
from TrainModel import trainModel

# args = {
#     "model": 'cmu',
#     "resize": '0x0',
#     "resize-out-ratio": float(4),
#     "tensorrt": "False"
# }

args=trainModel();

#    ______________    Recorded Video    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def RecordedVideoEvent(request):
    reqData = json.loads(request.body)
    print("Option: ", reqData['option'])
    print("File Path: ",reqData['url'])
    print("File Path: ", reqData['url'])
    return HttpResponse({'status': 200})


#    ______________    Kinect Live Stream    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def KinectLiveStreamEvent(request):
    reqData = json.loads(request.body)

    print('DATA: ', reqData)
    print("Option: ", reqData['option'])
    print("File Path: ", reqData['url'])

    return HttpResponse({'status': 200})


#    ______________    Camera Live Stream    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def CameraLiveStreamEvent(request):
    reqData = json.loads(request.body)

    print('DATA: ', reqData)
    print("Option: ", reqData['option'])
    print("File Path: ", reqData['url'])

    return HttpResponse({'status': 200})


#    ______________    Camera Static Image    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def CameraStaticImageEvent(request):
    reqData = json.loads(request.body)

    print('DATA: ', reqData)
    print("Option: ", reqData['option'])

    
    print("File Path: ", reqData['url'])
    pose = PoseEstimation(args=args, option=reqData['option'])

    try:
        keypoints = pose.getKeypoints()
    except:
        return JsonResponse({'status': 502})
    else:
        print("keypoints", keypoints)

        data = {
        "status": 200,
        "points": {'x': keypoints[0],
                    'y': keypoints[1],
                    'z': keypoints[2],
                   'image': reqData['url']}
    }
    return JsonResponse(data)


#    ______________    Static Image    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def StaticImageEvent(request):
    reqData = json.loads(request.body)

    print('DATA: ', reqData)
    print("Option: ", reqData['option'])
    print("File Path: ", reqData['url'])
    pose = PoseEstimation(args=args, option=reqData['option'], url=reqData['url'])

    try:
        keypoints = pose.getKeypoints()

    except:
        return JsonResponse({'status': 502})

    else:
        print("keypoints", keypoints)

        data = {
            "status": 200,
            "points": {'x': keypoints[0],
                       'y': keypoints[1],
                       'z': keypoints[2],
                       'image': reqData['url']}
        }
    return JsonResponse(data)


#    ______________    Save Routine Event    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def SaveRoutineEvent(request):

    reqData = json.loads(request.body)

    print('DATA: ',reqData)
    print(type(reqData))


    print(reqData['RoutineName'])
    for p in reqData['Points']:
        print(p)

    routine = Routine(name=reqData['RoutineName'])
    routine.save()
    for p in reqData['Points']:

        point = Points(points=p,routine=routine)
        point.save()
        print("point id: " , point.id)
        print("point routine id: " , point.routine.id)


    # rp = RobotProfile(name="Example 1")
    #
    # for e in reqData:
    #     print(e)
    #     p = Points(points=e, robotProfile=rp)
    #     print("Points PK: ", p.id)

    print(Routine.objects.all())
    print(Points.objects.all())

    return JsonResponse(reqData, safe=False)



#    ______________    Get All Routines Event    ______________________

@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def GetRoutinesEvent(request):
    # Points.objects.all()

    ResponsePointArray = []
    duplicateChecker = []

    LoadedPoints = json.loads(serializers.serialize('json', Points.objects.all()))
    for p in LoadedPoints:
        # print(p)
        # print(p['fields'])
        getRoutine = json.loads(serializers.serialize('json', Routine.objects.filter(pk=p['fields']['routine'])))
        getRoutineName = getRoutine[0]['fields']['name']

        getPoints = dict(eval(p['fields']['points']))
        routinePK = p['fields']['routine']

        if routinePK in duplicateChecker:
            for e in ResponsePointArray:
                if routinePK == e['routineID']:
                    e['points'].append(getPoints)

            pass
        else:
            ResponsePointArray.append({
                'routineName': getRoutineName,
                'points': [getPoints],
                'routineID': routinePK
            })
            duplicateChecker.append(routinePK)





    routineData = {'routineData': ResponsePointArray}

    return JsonResponse(routineData, safe=False)

#    ______________    Delete Routine Event    ______________________


@decorators.api_view(["DELETE"])
@decorators.permission_classes([permissions.AllowAny])
def DeleteRoutineEvent(request):

    reqData = json.loads(request.body)
    print(reqData)

    try:
        r = Routine.objects.get(id=reqData['routinePK'])
        print(r.delete())
    except:
        routineData = {'isDeleted': False, 'routine': reqData}
        print("Something went wrong and Rouitne not Deleted")
    else:
        routineData = {'isDeleted': True, 'routine': reqData}
        print("Nothing went wrong and Routine is Deleted")

    return JsonResponse(routineData, safe=False)


#    ______________    Update Routine Event    ______________________


@decorators.api_view(["PUT"])
@decorators.permission_classes([permissions.AllowAny])
def UpdateRoutineEvent(request):

    reqData = json.loads(request.body)
    print(reqData)


    r = Routine.objects.get(id=reqData['routineID'])
    r.name = reqData['newRoutineName']
    r.save()


    routineData = {'isUpdated': True}

    return JsonResponse(routineData, safe=False)

#    ______________    Save Robot Profile Event    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def SaveRobotProfileEvent(request):

    reqData = json.loads(request.body)

    print('DATA: ',reqData)



    profile = RobotProfile(name=reqData['ProfileName'], linkedRoutine=reqData['LinkedRoutine'])
    profile.save()



    return JsonResponse({'isSaved': True}, safe=False)


#    ______________    Get All Robot Profiles Event    ______________________

@decorators.api_view(["GET"])
@decorators.permission_classes([permissions.AllowAny])
def GetRobotProfilesEvent(request):

    Profiles = []
    rawProfiles = json.loads(serializers.serialize('json', RobotProfile.objects.all()))
    for p in rawProfiles:
        Profiles.append({'profilePK': p['pk'], 'profile': p['fields']})



    print(Profiles)



    return JsonResponse({'ProfilesList': Profiles}, safe=False)



#    ______________    Delete Robot Profile Event    ______________________


@decorators.api_view(["DELETE"])
@decorators.permission_classes([permissions.AllowAny])
def DeleteRobotProfileEvent(request):

    reqData = json.loads(request.body)
    print(reqData)

    try:
        r = RobotProfile.objects.get(id=reqData['profilePK'])
        print(r.delete())
    except:
        routineData = {'isDeleted': False, 'routine': reqData}
        print("Something went wrong and Rouitne not Deleted")
    else:
        routineData = {'isDeleted': True, 'routine': reqData}
        print("Nothing went wrong and Routine is Deleted")

    return JsonResponse(routineData, safe=False)


#    ______________    Update Robot Profile Event    ______________________


@decorators.api_view(["PUT"])
@decorators.permission_classes([permissions.AllowAny])
def UpdateRobotProfileEvent(request):

    reqData = json.loads(request.body)
    print(reqData)


    try:
        p = RobotProfile.objects.get(id=reqData['profilePK'])
        if reqData['ChangeLinking'] == True:
            p.linkedRoutine = reqData['linkedRoutine']
            p.save()
            routineData = {'isUpdated': True}
        elif reqData['ChangeLinking'] == False:
            p.name = reqData['NewProfileName']
            p.save()
            routineData = {'isUpdated': True}
    except:
        routineData = {'isUpdated': False}

    return JsonResponse(routineData, safe=False)

#    ______________    Get All Robot Profiles Along with Linked routines Event    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def GetRobotProfilesWithRoutineEvent(request):
    reqData = json.loads(request.body)
    print(reqData)

    ResponsePointArray = []
    duplicateChecker = []

    LoadedPoints = json.loads(serializers.serialize('json', Points.objects.all()))
    for p in LoadedPoints:
        # print(p)
        # print(p['fields'])
        getRoutine = json.loads(serializers.serialize('json', Routine.objects.filter(pk=p['fields']['routine'])))
        getRoutineName = getRoutine[0]['fields']['name']

        getPoints = dict(eval(p['fields']['points']))
        routinePK = p['fields']['routine']

        if routinePK in duplicateChecker:
            for e in ResponsePointArray:
                if routinePK == e['routineID']:
                    e['points'].append(getPoints)

            pass
        else:
            ResponsePointArray.append({
                'routineName': getRoutineName,
                'points': [getPoints],
                'routineID': routinePK
            })
            duplicateChecker.append(routinePK)

    # routineData = {'routineData': ResponsePointArray}

    routine = {}

    for e in ResponsePointArray:
        if e['routineID'] == reqData['routinePK']:
            routine = e
            break

    print(routine)

    return JsonResponse(routine, safe=False)


#    ______________    Trigger Webots Simulation Event    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def TriggerWebotsSimEvent(request):
    reqData = json.loads(request.body)
    print(reqData)
    print("Webots Simulation Event Triggered!")

    errorCheckStatus = False
    errorMessage = ''

    s = socket.socket()
    print("Socket successfully created")
    port = 4096
    try:
        s.bind(('', port))
        print("socket binded to %s" % (port))
        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")
    except Exception as e:
        errorCheckStatus = True
        errorMessage = str(e)
        print(str(e))
        # print("Something went wrong")
    finally:
        # s.close()
        if errorCheckStatus == False:
            while True:
                c, addr = s.accept()
                print('Got connection from', addr)
                reply = 'Thank you for connecting'
                command = 'MOVE_L | 3.0 | 35'
                c.send(command.encode('utf-8'))
                c.close()





    data = {'errorMessage': errorMessage, 'errorCheckStatus': errorCheckStatus}

    return JsonResponse(data, safe=False)

#    ______________    Trigger UR Simulation Event    ______________________

@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def TriggerURSimEvent(request):
    reqData = json.loads(request.body)
    print(reqData)
    print("UR Simulation Event Triggered!")

    return JsonResponse({}, safe=False)