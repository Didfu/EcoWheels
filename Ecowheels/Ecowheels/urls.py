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
from django.urls import path
import main.views as mviews
import authapp.views as aviews
import adminapp.views as adviews


urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('', aviews.landingpage, name="landingpage"),
    # path('home/', aviews.landingpage, name='home'),
    path('login/', aviews.loginpage, name='login'), 
    path('signup/', aviews.signuppage, name="signup"),
    path('logout/', aviews.user_logout, name='logout'),
    path('forgotpassword/', aviews.ForgotPassword, name='forgotpassword'),
    path('ChangePassword/<uuid:token>/', aviews.ChangePassword, name='changepassword'),
]

adminapp = [
    path('addstore/', adviews.addstore,name='addstore'),
    path('feedback/', adviews.addstore,name='feedback'),
    path('adminlogin/', adviews.addstore,name='adminlogin'),
]

urlpatterns = main + auth + adminapp + urlpatterns