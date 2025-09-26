from django.shortcuts import render,redirect
from events.forms import CategoryModelForm,EventModelForm,ParticipantModelForm,GroupCreationForm
from events.models import Category,Event
from django.db.models import Count,Q
import datetime
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,DetailView,UpdateView,CreateView
User=get_user_model()
# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()
def is_participant(user):
    return user.groups.filter(name='Participant').exists()
def both(user):
    return is_admin(user) or is_organizer(user)
@login_required
@user_passes_test(both,login_url='no-access')
def home(request):
    past_events=Event.objects.filter(date__lt=datetime.date.today()).annotate(total_participants=Count('participants'))
    nearest_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    nearest_count = nearest_event.participants.count() if nearest_event else 0
    categories=Category.objects.all()
    context={
        'past_events':past_events,
        'nearest_event':nearest_event,
        'nearest_count':nearest_count,
        'categories':categories,
    }
    return render(request,'home.html',context)



both_access=[ login_required , user_passes_test(both,login_url='no-access')]
@method_decorator(both_access,name='dispatch')
class Home(TemplateView):
    template_name='home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        past_events=Event.objects.filter(date__lt=datetime.date.today()).annotate(total_participants=Count('participants'))
        nearest_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
        nearest_count = nearest_event.participants.count() if nearest_event else 0
        categories=Category.objects.all()
        context["past_events"] = past_events
        context["nearest_event"] =nearest_event
        context["nearest_count"] =nearest_count
        context["categories"] =categories
        return context
    



@login_required
@user_passes_test(both,login_url='no-access')
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



@method_decorator(both_access,name='dispatch')
class CategoryFilter(DetailView):
    pk_url_kwarg='id'
    model=Category
    template_name='filter.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events=Event.objects.filter(category=self.object).annotate(total_participants=Count('participants'))
        categories=Category.objects.all()
        context["events"] = events
        context["categories"] = categories
        context["title"] = self.object.name
        return context
    

@login_required
@user_passes_test(both,login_url='no-access')
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


@method_decorator(both_access, name='dispatch')
class SearchFilter(TemplateView):
    template_name = 'filter.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.request.GET.get('res','')
        events = Event.objects.filter(name__icontains=result).annotate(
            total_participants=Count('participants')
        )
        categories = Category.objects.all()
        context['events'] = events
        context['categories'] = categories
        context['title'] = 'Search Result'
        return context
    



@login_required
@user_passes_test(both,login_url='no-access')
def dashboard(request):
    total_participant=User.objects.filter(events__isnull=False).count()
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




@login_required
@user_passes_test(both,login_url='no-access')
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

@method_decorator(both_access, name='dispatch')
class CreateCategory(CreateView):
    model = Category
    form_class = CategoryModelForm
    template_name = 'form.html'
    success_url = reverse_lazy('create-category')

    def form_valid(self, form):
        messages.success(self.request, 'Category Created Successfully!!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Category'
        return context
    

@login_required
@user_passes_test(both,login_url='no-access')
def create_event(request):
    if request.method == 'POST':
        event=EventModelForm(request.POST,request.FILES)
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



@method_decorator(both_access, name='dispatch')
class CreateEvent(CreateView):
    model = Event
    form_class = EventModelForm
    template_name = 'form.html'
    success_url = reverse_lazy('create-event')

    def form_valid(self, form):
        messages.success(self.request, 'Event Created Successfully!!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Event'
        return context



@login_required
@user_passes_test(is_admin,login_url='no-access')
def group_page(request):
    groups=Group.objects.all()
    return render(request,'group.html',{'groups': groups})

@login_required
@user_passes_test(is_admin,login_url='no-access')
def delete_group(request,grp_id):
    if request.method=="POST":
        group=Group.objects.get(id=grp_id)
        group.delete()
        messages.success(request,'Group deleted Successfully!!')
        return redirect('group-page')

def create_participant(request):
    if request.method == 'POST':
        form=ParticipantModelForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request,'Account Created Successfully!! Check your mail for Activate your account')
            return redirect('login-page')
        else:
            messages.success(request,'Something went Wrong!!')
            return redirect('create-participant')
    context={
        'form':ParticipantModelForm,
        'type':'Participant'
    }
    return render(request,'form.html',context)

@login_required
@user_passes_test(is_admin,login_url='no-access')
def show_participant(request):
    participants=User.objects.all()
    groups=Group.objects.all()
    return render(request,'participants.html',{'participants':participants,'groups':groups})


@login_required
@user_passes_test(is_admin,login_url='no-access')
def delete_participant(request,user_id):
    if request.method=='POST':
        user=User.objects.get(id=user_id)
        user.delete()
        messages.success(request,'Participant Deleted Successfully!')
        return redirect('participant-page')
@login_required
@user_passes_test(is_admin,login_url='no-access')   
def update_participant(request,user_id):
    if request.method=='POST':
        user=User.objects.get(id=user_id)
        grp_id=request.POST.get('group')
        if grp_id:
            
            grp=Group.objects.get(id=grp_id)
            user.groups.clear()
            user.groups.add(grp)
            user.save()
            messages.success(request,'Role updated Successfully')
            return redirect('participant-page')
        else:
            messages.success(request,'Something Wrong! Try again')
            return redirect('participant-page')
@login_required
@user_passes_test(is_admin,login_url='no-access')
def create_group(request):
    if request.method=='POST':
        form=GroupCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Group Created Successfully!!')
            return redirect('create-group')
    
    context={
        'form':GroupCreationForm,
        'type':'Group'
    }
    return render(request,'form.html',context)





@login_required
@user_passes_test(both,login_url='no-access')
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


@login_required
@user_passes_test(both,login_url='no-access')
def delete_event(request,id):
    e=Event.objects.get(id=id)
    if request.method == 'POST':
        e.delete()
        messages.success(request,'Event deleted Successfully')
        return redirect('dashboard')
    else:
        return redirect('dashboard')
@login_required
@user_passes_test(is_participant,login_url='no-access')   
def event_rsvp(request,user_id,event_id):
    if request.method=='POST':
        user=User.objects.get(id=user_id)
        event=Event.objects.get(id=event_id)
        user.events.add(event)
        return redirect('participant-home')
    
def account_activate(request,user_id,token):
    try:
        user=User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,'Activation complete now you can login')
            return redirect('login-page')
        else:
            return redirect('no-access')
    except User.DoesNotExist:
        return redirect('no-access')
