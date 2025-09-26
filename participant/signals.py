from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

User=get_user_model()



@receiver(post_save,sender=User)
def user_creation(sender,instance,created,**kwargs):
    if created:
        token=default_token_generator.make_token(instance)
        activation_url=f'{settings.FRONTEND_URL}/events/activate/{instance.id}/{token}'
        subject='Account activation'
        message=f'Hello {instance.first_name} !\nTo activate your account please click the link below\n\n{activation_url}\n\nThank You!'
        send_mail(
            subject,
            message,
            "abc.software.io@gmail.com",
            [instance.email],
            fail_silently=False,
        )
        user_grp,created=Group.objects.get_or_create(name='Participant')
        instance.groups.add(user_grp)

@receiver(m2m_changed,sender=User.events.through)
def rsvp_confirmation(sender,instance,action,**kwargs):
    if action=='post_add':
        send_mail(
            'Event Booking confirmation',
            f'Hello {instance.username}\nThanks for your participation\nhope you will enjoy\n\nThank you :)',
            "abc.software.io@gmail.com",
            [instance.email],
            fail_silently=False,
        )