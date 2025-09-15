from django.shortcuts import render,redirect
from events.forms import CategoryModelForm,ParticipantModelForm,EventModelForm
from events.models import Category,Event,Participant
from django.db.models import Count,Q
import datetime
from django.contrib import messages
# Create your views here.

def home(request):
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
    return render(request,'home.html',context)


def category_filter(request,id):
    c=Category.objects.get(id=id)
    events=Event.objects.filter(category=c).annotate(total_participants=Count('participants'))
    categories=Category.objects.all()
    context={
        'events':events,
        'categories':categories,
        'title':c.name
    }
    return render(request,'filter.html',context)

def search_filter(request):
    result=request.GET.get('res')
    events=Event.objects.filter(name__icontains=result).annotate(total_participants=Count('participants'))
    categories=Category.objects.all()
    context={
        'events':events,
        'categories':categories,
        'title':'Search Result'
    }
    return render(request,'filter.html',context)





def dashboard(request):
    total_participant=Participant.objects.filter(events__isnull=False).count()
    events = Event.objects.select_related("category").prefetch_related("participants").annotate(
        total=Count('participants')
    ).all()
    categories=Category.objects.all()
    events_count=Event.objects.aggregate(
        total_event=Count('id'),
        total_upcoming=Count('id',filter=Q(date__gt=datetime.date.today())),
        total_past=Count('id',filter=Q(date__lt=datetime.date.today())),
    )
    type=request.GET.get('type')
    if type=='Upcoming':
        events=events.filter(date__gt=datetime.date.today())
        context={
            'total_participant':total_participant,
            'events_count':events_count,
            'events':events,
            'title':'Upcoming Events',
            'categories':categories,
        }
        return render(request,'dashboard.html',context)
    
    elif type=='Past':
        events=events.filter(date__lt=datetime.date.today())
        context={
            'total_participant':total_participant,
            'events_count':events_count,
            'events':events,
            'title':'Past Events',
            'categories':categories,
        }
        return render(request,'dashboard.html',context)
    
    elif type=='Total':
        context={
            'total_participant':total_participant,
            'events_count':events_count,
            'events':events,
            'title':'Total Events',
            'categories':categories,
        }
        return render(request,'dashboard.html',context)
    


    events=events.filter(date=datetime.date.today())
    context={
        'total_participant':total_participant,
        'events_count':events_count,
        'events':events,
        'title':"Today's Events",
        'categories':categories,
    }
    return render(request,'dashboard.html',context)





def create_category(request):
    if request.method == 'POST':
        categor=CategoryModelForm(request.POST)
        if categor.is_valid():
            categor.save()
            messages.success(request,'Category Created Successfully!!')
            return redirect('create-category')
        else:
            messages.success(request,'Something went Wrong!!')
            return redirect('create-category')
    context={
        'form':CategoryModelForm,
        'type':'Category'
    }
    return render(request,'form.html',context)





def create_event(request):
    if request.method == 'POST':
        event=EventModelForm(request.POST)
        if event.is_valid():
            event.save()
            messages.success(request,'Event Created Successfully!!')
            return redirect('create-event')
        else:
            messages.success(request,'Something went Wrong!!')
            return redirect('create-event')
    context={
        'form':EventModelForm,
        'type':'Event'
    }
    return render(request,'form.html',context)



def create_participant(request):
    if request.method == 'POST':
        participant=ParticipantModelForm(request.POST)
        if participant.is_valid():
            participant.save()
            messages.success(request,'Participant Created Successfully!!')
            return redirect('create-participant')
        else:
            messages.success(request,'Something went Wrong!!')
            return redirect('create-participant')
    context={
        'form':ParticipantModelForm,
        'type':'Participant'
    }
    return render(request,'form.html',context)


def update_event(request,id):
    e=Event.objects.get(id=id)
    if request.method == 'POST':
        event=EventModelForm(request.POST,instance=e)
        if event.is_valid():
            event.save()
            messages.success(request,'Event updated Successfully!!')
            return redirect('create-event')
    context={
        'form':EventModelForm(instance=e),
        'type':'Event'
    }
    return render(request,'form.html',context)

def delete_event(request,id):
    e=Event.objects.get(id=id)
    if request.method == 'POST':
        e.delete()
        messages.success(request,'Event deleted Successfully')
        return redirect('create-event')
    else:
        return redirect('home')