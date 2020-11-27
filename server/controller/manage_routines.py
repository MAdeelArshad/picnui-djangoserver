import argparse

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import response, decorators, permissions, status
import json
import random

from PoseDetection import PoseEstimation

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
from server.models import RobotProfile, Points

args = {
    "model": 'cmu',
    "resize": '0x0',
    "resize-out-ratio": float(4),
    "tensorrt": "False"
}


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

    # rp = RobotProfile(name="Example 1")
    #
    # for e in reqData:
    #     print(e)
    #     p = Points(points=e, robotProfile=rp)
    #     print("Points PK: ", p.id)

    return JsonResponse(reqData, safe=False)
