from django.shortcuts import render

# Create your views here.
def signup(request):
    return render (request,'auth/signup.html')

def login(request):
    return render (request,'auth/login.html')

def changepass(request):
    return render (request,'auth/changepass.html')

def forgotpass(request):
    return render (request,'auth/forgotpass.html')

def landingpage(request):
    return render (request,'auth/landingpage.html')