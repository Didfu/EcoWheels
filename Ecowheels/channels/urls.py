from django.urls import path
from . import views

urlpatterns = [
    path('<int:channel_id>/', views.channel_detail, name='channel_detail'),
]
