from django.shortcuts import render,redirect
from events.forms import CategoryModelForm,EventModelForm,ParticipantModelForm,GroupCreationForm
from events.models import Category,Event
from django.db.models import Count,Q
import datetime
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from events.views import both
from django.contrib.auth.decorators import login_required,user_passes_test

User=get_user_model()



@login_required
@user_passes_test(both, login_url='no-access')
def organizer_home(request):
    all_events = Event.objects.all().annotate(total_participants=Count('participants'))
    
    nearest_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    nearest_count = nearest_event.participants.count() if nearest_event else 0
    
    categories = Category.objects.all()
    
    context = {
        'past_events': all_events, 
        'nearest_event': nearest_event,
        'nearest_count': nearest_count,
        'categories': categories,
    }
    
    return render(request, 'organizer_home.html', context)