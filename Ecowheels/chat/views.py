from django.shortcuts import render

def chat_room(request):
    return render(request, 'chat/chat.html')
