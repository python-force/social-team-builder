from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from stb.core.models import Profile, Skill, Project, Position
from django import forms

# ProfileFormSet = inlineformset_factory(Profile, Skill, fields = ['profile', 'title'], can_delete = True)

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "What would be your username?"
        self.fields["email"].label = "What would be your email address?"


class SkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control-sm form-control'})

    class Meta:
        model = Skill
        fields = ['title']


class PositionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control-sm form-control'})
        self.fields['description'].widget = forms.Textarea({'class': 'form-control'})
        self.fields['availability'].widget.attrs.update({'class': 'form-control-sm form-control'})

    class Meta:
        model = Position
        fields = ['title', 'description', 'availability']


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea({'class': 'form-control'})
        self.fields['timeline'].widget.attrs.update({'class': 'form-control'})
        self.fields['applicant_requirements'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Project
        fields = ['title', 'url', 'description', 'timeline', 'applicant_requirements']

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget = forms.Textarea({'class': 'form-control'})
        self.fields['other_skills'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Profile
        fields = ['full_name', 'description', 'avatar', 'other_skills']
