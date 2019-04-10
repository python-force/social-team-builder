from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from stb.core.models import Profile, Skill, Project
from stb.core.forms import UserCreateForm
from django.http import Http404
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory


class Homepage(TemplateView):
    template_name = "index.html"

class ProjectView(TemplateView):
    template_name = "project.html"

class ProjectUpdateView(TemplateView):
    template_name = "project_edit.html"

class ProjectNewView(TemplateView):
    template_name = "project_new.html"

class Applications(TemplateView):
    template_name = "applications.html"

class ProfileView(TemplateView):
    template_name = "profile.html"

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user=self.request.user)
            return context
        except:
            raise Http404


class SkillInline(InlineFormSetFactory):
    model = Skill
    fields = ['title',]
    initial = [{'title': 'Enter Skill'}]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}

class ProjectInline(InlineFormSetFactory):
    model = Project
    fields = ['title', 'url']
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}

class ProfileUpdateView(UpdateWithInlinesView):
    model = Profile
    inlines = [SkillInline, ProjectInline]
    fields = ['full_name', 'description', 'avatar']
    template_name = 'profile_edit.html'

    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def get_object(self, queryset=None):
        return self.get_queryset()

"""
class ProfileUpdateView(UpdateView):
    template_name = "profile_edit.html"
    model = Profile
    fields = ['full_name', 'description']

    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def get_object(self, queryset=None):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_formset'] = ProfileFormSet(self.request.POST, instance=self.object)
            context['profile_formset'].full_clean()
        else:
            context['profile_formset'] = ProfileFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context['profile_formset']
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            return response
        else:
            return super().form_invalid(form)
"""

"""
class ProfileUpdateView(TemplateView):
    template_name = "profile_edit.html"

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = Profile.objects.get(user=self.request.user)
            return context
        except:
            raise Http404
"""

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"