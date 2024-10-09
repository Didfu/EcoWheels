from django.shortcuts import render

# Create your views here.
def logtrip(request):
    return render(request,'main/tips.html')

def home(request):
    return render (request,'main/home.html')

def redeem(request):
    return render (request,'main/redeem.html')

def leaderboard(request):
    return render (request,'main/leaderboard.html')

def carpooling(request):
    return render (request,'main/carpooling.html')

def profile(request):
    return render (request,'main/profile.html')

def tips(request):
    return render (request,'main/tips.html')