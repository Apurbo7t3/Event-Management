from django.shortcuts import render,redirect
from events.forms import CategoryModelForm,EventModelForm,ParticipantModelForm,GroupCreationForm
from events.models import Category,Event
from django.db.models import Count,Q
import datetime
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from events.views import is_participant
from django.contrib.auth.decorators import login_required,user_passes_test



@login_required
@user_passes_test(is_participant,login_url='no-access')
def participant_home(request):
    past_events=Event.objects.filter(date__gte=datetime.date.today()).annotate(total_participants=Count('participants'))
    nearest_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    nearest_count=nearest_event.participants.count()
    categories=Category.objects.all()
    context={
        'past_events':past_events,
        'nearest_event':nearest_event,
        'nearest_count':nearest_count,
        'categories':categories,
    }
    return render(request,'participant_home.html',context)

@login_required
@user_passes_test(is_participant,login_url='no-access')
def participant_category_filter(request,id):
    c=Category.objects.get(id=id)
    events=Event.objects.filter(category=c).annotate(total_participants=Count('participants'))
    categories=Category.objects.all()
    context={
        'events':events,
        'categories':categories,
        'title':c.name
    }
    return render(request,'participant_filter.html',context)

@login_required
@user_passes_test(is_participant,login_url='no-access')
def participant_search_filter(request):
    result=request.GET.get('res')
    events=Event.objects.filter(name__icontains=result).annotate(total_participants=Count('participants'))
    categories=Category.objects.all()
    context={
        'events':events,
        'categories':categories,
        'title':'Search Result'
    }
    return render(request,'participant_filter.html',context)

@login_required
@user_passes_test(is_participant,login_url='no-access')
def participant_dashboard(request, user_id):
    user=User.objects.get(id=user_id)
    events=Event.objects.filter(participants=user).select_related("category").prefetch_related("participants").annotate(total=Count("participants"))
    categories = Category.objects.all()

    context = {
        "events": events,
        "categories": categories,
        "selected_user": user,
    }
    return render(request, "participant_dashboard.html", context)
