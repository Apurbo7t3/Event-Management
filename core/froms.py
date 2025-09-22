from django.contrib.auth.forms import AuthenticationForm
from events.forms import FormMixin
class LoginForm(FormMixin,AuthenticationForm):
      def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style()