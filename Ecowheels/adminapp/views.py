from django.shortcuts import render

# Create your views here.
def adminlogin(request):
    return render (request,'admin/adminlogin.html')

def addstore(request):
    return render (request,'admin/addstore.html')

def feedback(request):
    return render (request,'admin/feedback.html')