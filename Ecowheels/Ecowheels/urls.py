"""
URL configuration for Ecowheels project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import main.views as mviews
import authapp.views as aviews
import adminapp.views as adviews
from chat import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('', mviews.home, name='home'),
]

main = [
    path('logtrip/', mviews.logtrip,name='logtrip'),
    path('home/', mviews.home,name='home'),
    path('redeem/', mviews.redeem,name='redeem'),
    path('leaderboard/', mviews.leaderboard,name='leaderboard'),
    path('carpooling/', mviews.carpooling,name='carpooling'),
    path('profile/', mviews.profile,name='profile'),
    path('tips/', mviews.tips,name='tips'),
]

auth = [
path('/', aviews.landingpage,name='landingpage'),
path('changepass/', aviews.changepass,name='changepass'),
path('forgotpass/', aviews.forgotpass,name='forgotpass'),
path('signup/', aviews.signup,name='signup'),
path('login/', aviews.login,name='login'),
]

adminapp = [
    path('addstore/', adviews.addstore,name='addstore'),
    path('feedback/', adviews.addstore,name='feedback'),
    path('adminlogin/', adviews.addstore,name='adminlogin'),
]

chat = [
    path('chat_room/', views.chat_room, name='chat_room'),
]
channels = [
    path('chat/', include('chat.urls')),
]
urlpatterns = main+auth+adminapp+chat+channels+urlpatterns