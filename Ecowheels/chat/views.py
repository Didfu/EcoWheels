from django.shortcuts import render

def chatroom(request, room_name):
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name
    })
