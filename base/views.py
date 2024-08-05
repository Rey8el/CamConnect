from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random 
import time
import json
from .models import RoomMember

from django.views.decorators.csrf import csrf_exempt
#Build token with uid

# Create your views here.

def getToken(request):
    appId = "c19743dcba68437ba41956a72a1264dc"
    appCertificate = "58c66466220049899432cf38148aa187"
    channelName = request.GET.get('channel') 
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600 * 48
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe = False)





def lobby(request):
    return render(request,'base/lobby.html')
def room(request):
    return render(request,'base/room.html')


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid = data['UID'],
        room_name = data['room-name']
    )
    return JsonResponse({'name':data['name']},safe = False)


def get_member(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    try:
        member = RoomMember.objects.get(
            uid=uid,
            room_name=room_name,
        )
        return JsonResponse({'name': member.name}, safe=False)
    except RoomMember.DoesNotExist:
        return JsonResponse({'name': 'Unknown'}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid = data['UID'],
        room_name=data['room_name'],
    )
    member.delete()
    return JsonResponse('Member was deleted',safe = False)

