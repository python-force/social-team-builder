from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from stb.core.models import Profile, Skill, Project, Position
from stb.core.forms import UserCreateForm
from django.http import Http404
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.http import HttpResponseRedirect
from django.forms.formsets import all_valid

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class Homepage(TemplateView):
    template_name = "index.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['profile'] = Profile.objects.get(user=self.request.user)
        projects = Project.objects.all()
        context['projects'] = projects
        positions = []
        for project in projects:
            for position in project.positions.all():
                if position.title not in positions:
                    positions.append(position.title)
        print(positions)
        context['positions'] = positions
        return context

class ProjectView(TemplateView):
    template_name = "project.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['project'] = Project.objects.get(id=self.kwargs.get('pk'))
        context['positions'] = context['project'].positions.all()
        return context

class Applications(TemplateView):
    template_name = "applications.html"

class ProfileView(TemplateView):
    template_name = "profile.html"

class ProfileView(TemplateView):
    template_name = "profile.html"

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user=self.request.user)
            context['skills'] = context['profile'].skills.all()
            context['projects'] = context['profile'].projects.all()
            return context
        except:
            raise Http404


class SkillInline(InlineFormSetFactory):
    model = Skill
    fields = ['title',]
    initial = [{'title': 'Enter Skill'}]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'skill_formset'


class ProjectInline(InlineFormSetFactory):
    model = Project
    fields = ['title', 'url']
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'project_formset'


class ProfileUpdateView(UpdateWithInlinesView):
    model = Profile
    inlines = [SkillInline, ProjectInline]
    fields = ['full_name', 'description', 'avatar']
    template_name = 'profile_edit.html'

    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def get_object(self, queryset=None):
        return self.get_queryset()


class PositionInline(InlineFormSetFactory):
    model = Position
    fields = ['title', 'description']
    initial = [{'title': 'Enter Position'}]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'position_formset'

class CreateProjectView(CreateWithInlinesView):
    model = Project
    inlines = [PositionInline]
    fields = ['title', 'description', 'timeline', 'applicant_requirements']
    template_name = 'project_new.html'

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object.profile = self.request.user.profile
        return super().forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProjectUpdateView(UpdateWithInlinesView):
    model = Project
    inlines = [PositionInline]
    fields = ['title', 'description', 'timeline', 'applicant_requirements']
    template_name = 'project_edit.html'

    def get_queryset(self):
        return Project.objects.get(id=self.kwargs.get('pk'))

    def get_object(self, queryset=None):
        return self.get_queryset()
