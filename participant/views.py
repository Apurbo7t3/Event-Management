from django.shortcuts import render, redirect, get_object_or_404
from events.forms import CategoryModelForm, EventModelForm, ParticipantModelForm, GroupCreationForm
from events.models import Category, Event
from django.db.models import Count
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test

User = get_user_model()

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists(), login_url='no-access')
def participant_home(request):
    today = datetime.date.today()

    nearest_event = Event.objects.filter(date__gte=today).order_by('date').first()
    nearest_count = nearest_event.participants.count() if nearest_event else 0

    all_events = Event.objects.all().annotate(total_participants=Count('participants'))
    
    if nearest_event:
        all_events = all_events.exclude(id=nearest_event.id)

    categories = Category.objects.all()

    context = {
        'nearest_event': nearest_event,
        'nearest_count': nearest_count,
        'past_events': all_events, 
        'categories': categories,
    }
    return render(request, 'participant_home.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists(), login_url='no-access')
def participant_category_filter(request, id):
    category = get_object_or_404(Category, id=id)
    events = Event.objects.filter(category=category)\
                .annotate(total_participants=Count('participants'))
    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories,
        'title': category.name
    }
    return render(request, 'participant_filter.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists(), login_url='no-access')
def participant_search_filter(request):
    result = request.GET.get('res', '')
    events = Event.objects.filter(name__icontains=result)\
                .annotate(total_participants=Count('participants'))
    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories,
        'title': f'Search Results for "{result}"'
    }
    return render(request, 'participant_filter.html', context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Participant').exists(), login_url='no-access')
def participant_dashboard(request, user_id):
    user = get_object_or_404(User, id=user_id)
    events = Event.objects.filter(participants=user)\
                .select_related('category')\
                .prefetch_related('participants')\
                .annotate(total=Count('participants'))
    categories = Category.objects.all()
    context = {
        'events': events,
        'categories': categories,
        'selected_user': user,
    }
    return render(request, 'participant_dashboard.html', context)


@login_required
def profile(request):
    return render(request, 'participant_profile.html')