from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from core.forms import LoginForm
from events.views import is_admin,is_organizer,is_participant
from django.views.generic import UpdateView,TemplateView
from participant.models import CustomUser
from core.forms import EditProfileForm,PassChangeForm,PassResetForm,PassResetConfirmForm
from django.contrib.auth.views import PasswordChangeView,PasswordResetView,PasswordResetConfirmView

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

class EditProfileView(UpdateView):
    model=CustomUser
    form_class=EditProfileForm
    template_name='edit.html'
    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Info Updated Successfully!!')
        return redirect('edit-profile')


class PassChangeView(PasswordChangeView):
    template_name='edit.html'
    form_class = PassChangeForm
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request,'Your Password Change successfully!!')
        return super().form_valid(form)
    

class PassResetView(PasswordResetView):
    form_class=PassResetForm
    template_name='edit.html'
    success_url=reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(self.request,'A password Reset mail is sent to your Accout')
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["protocol"] = 'https' if self.request.is_secure() else 'http'
        context['domain']=self.request.get_host()
        return context

class PassResetConfirmView(PasswordResetConfirmView):
    template_name= 'registration/password_reset.html'
    form_class=PassResetConfirmForm
    success_url = reverse_lazy('sign-in')
    def form_valid(self, form):
        messages.success(self.request,'Your password reset successfuly!')
        return super().form_valid(form)

class ProfileView(TemplateView):
    template_name='profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["name"] = user.get_full_name()
        context["username"] = user.username
        context["designation"] = user.groups.first().name
        context["email"] = user.email
        context["phone"] = user.phone_number
        context["bio"] = user.bio
        context["image"] = user.profile_image.url
        return context
    