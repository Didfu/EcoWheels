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
from django.conf import settings
from django.conf.urls.static import static
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
    path('carpooling-chat/', mviews.carpooling_chat, name='carpooling_chat'),
    path('tips/', mviews.tips,name='tips'),
     path('process_form/',mviews.process_form,name='process_form'),
     path('get-personalized-recommendations/', mviews.get_personalized_recommendations, name='get_personalized_recommendations'),
     path('submit_feedback/',mviews.submit_feedback,name='submit_feedback'),

]

auth = [
    path('', aviews.landingpage, name="landingpage"),
    path('login/', aviews.loginpage, name='login'),     
    path('signup/', aviews.signuppage, name="signup"),
    path('logout/', aviews.user_logout, name='logout'),
    path('forgotpassword/', aviews.ForgotPassword, name='forgotpassword'),
    path('ChangePassword/<uuid:token>/', aviews.ChangePassword, name='changepassword'),
    path('view_profile/<int:user_id>/', aviews.view_profile, name='view_profile'),
    path('edit_profile/<int:user_id>/', aviews.edit_profile, name='edit_profile'),
    path('avatar_selection/', aviews.avatar_selection, name='avatar_selection'),
    path('update-avatar/', aviews.update_avatar, name='update_avatar'),
    path('add_friend/<int:user_id>/', aviews.add_friend, name='add_friend'),
    path('friends_list/', aviews.friends_list, name='friends_list'),
    path('accept_request/<int:request_id>/', aviews.accept_request, name='accept_request'),
    path('decline_request/<int:request_id>/', aviews.decline_request, name='decline_request'),
    path('search/', aviews.search_users, name='search_users'),

]

adminapp = [
path('admin_login/', adviews.adminlogin, name='adminlogin'),
path('view_feedback/', adviews.view_feedback, name='view_feedback'),
path('add_store/', adviews.add_store, name='addstore'),
path('admin_logout',adviews.admin_logout,name='adlogout'),
path('manage-stores/', adviews.manage_stores, name='manage_stores'),
path('edit-store/<int:store_id>/', adviews.edit_store, name='edit_store'),
path('delete-store/<int:store_id>/', adviews.delete_store, name='delete_store'),
]

urlpatterns = main + auth + adminapp + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)