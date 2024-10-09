from django.shortcuts import render, get_object_or_404
from .models import Channel

def channel_detail(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    messages = channel.channelmessage_set.all()
    return render(request, 'channels/channel_detail.html', {'channel': channel, 'messages': messages})
