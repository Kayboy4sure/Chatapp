from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'room': room,
        'username': username,
        'room_details': room_details})


def check_view(request):
    room_name = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room_name).exists():
        return redirect('/' + room_name + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/' + room_name + '/?username=' + username)


def send(request):
    username = request.POST['username']
    room_id = request.POST['room_id']
    message = request.POST['message']

    new_message = Message.objects.create(content=message, username=username, room=room_id)
    new_message.save()
    return HttpResponse('message successfully sent')


def get_message(request, room):
    room_detail = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_detail.id)
    return JsonResponse({'messages': list(messages.values())})
