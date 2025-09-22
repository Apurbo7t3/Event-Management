from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from core.froms import LoginForm
from events.views import is_admin,is_organizer,is_participant
# Create your views here.
def sign_in(request):
    return render(request,'sign_in.html')
def sign_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('sign-in')
def user_login(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            if is_admin(user):
                return redirect('home')
            elif is_organizer(user):
                return redirect('organizer-home')
            elif is_participant(user):
                return redirect('participant-home')
            else:
                messages.success(request,'Something went wrong please try again!')
                return redirect('login-page')
    return render(request,'login_page.html',{'form':form})

def no_access(request):
    return render(request,'no_access.html')