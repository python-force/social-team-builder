from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from stb.core.models import Profile, Skill

# ProfileFormSet = inlineformset_factory(Profile, Skill, fields = ['profile', 'title'], can_delete = True)

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "What would be your username?"
        self.fields["email"].label = "What would be your email address?"