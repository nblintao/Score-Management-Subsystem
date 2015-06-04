from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
	#Pick a course push modify button
	return HttpResponse("Check in box and notify")

def modify(request):
	#Make modify and check
	return HttpResponse("make modify on website and refresh notifySender/Receiver")

def vote(request):
	#Vote
	return HttpResponse("Confirm vote")
	
