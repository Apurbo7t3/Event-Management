from django.shortcuts import render,redirect
from events.forms import CategoryModelForm,EventModelForm,ParticipantModelForm,GroupCreationForm
from events.models import Category,Event
from django.db.models import Count,Q
import datetime
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
# Create your views here.
from events.views import both
from django.contrib.auth.decorators import login_required,user_passes_test
@login_required
@user_passes_test(both,login_url='no-access')
def organizer_home(request):
    past_events=Event.objects.filter(date__lt=datetime.date.today()).annotate(total_participants=Count('participants'))
    nearest_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    nearest_count=nearest_event.participants.count()
    categories=Category.objects.all()
    context={
        'past_events':past_events,
        'nearest_event':nearest_event,
        'nearest_count':nearest_count,
        'categories':categories,
    }
    return render(request,'organizer_home.html',context)