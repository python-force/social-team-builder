from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from stb.core.models import Profile, Skill, Project, Position, Position_Application
from stb.core.forms import UserCreateForm
from django.http import Http404
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
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
        profile = Profile.objects.get(user=self.request.user)
        projects = Project.objects.all()
        context['projects'] = projects
        context['positions'] = Position.objects.filter(project__profile=profile.id).order_by('title').distinct('title')
        return context


class Applications(TemplateView):
    template_name = "applications.html"


class ProfileSkillInline(InlineFormSetFactory):
    model = Skill.profile.through
    exclude = ['id']


class SkillInline(InlineFormSetFactory):
    model = Skill
    inlines = [ProfileSkillInline]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'skill_formset'


class ProjectInline(InlineFormSetFactory):
    model = Project
    fields = ['title', 'url']
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'project_formset'


class ProfileView(TemplateView):
    template_name = "profile.html"

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile
            context['skills'] = profile.skills.all()
            context['projects'] = profile.projects.all()
            return context
        except:
            raise Http404


class ProfileUpdateView(UpdateWithInlinesView):
    model = Profile
    inlines = [ProfileSkillInline, ProjectInline]
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


class ProjectNeedsView(TemplateView):
    template_name = "project-needs.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = Position.objects.get(id=self.kwargs.get('pk'))
        context["position"] = position
        context["projects"] = Project.objects.all().filter(positions__title=position.title)
        return context


class ProjectView(TemplateView):
    template_name = "project.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['project'] = Project.objects.get(id=self.kwargs.get('pk'))
        positions = context['project'].positions.all()
        context['positions'] = positions
        applied = []
        for position in positions:
            try:
                found = Position_Application.objects.get(user=self.request.user, position=position)
                applied.append(found.position.id)
            except:
                pass
        context['applied'] = applied
        return context

class ApplyPositionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("project",
                       kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        position = get_object_or_404(Position, id=self.kwargs.get("position"))

        try:
            obj, created = Position_Application.objects.get_or_create(
                user=self.request.user,
                position=position,
                status=0
            )
        except IntegrityError:
            messages.warning(
                self.request,
                ("You have already applied for {} "
                 "position").format(
                    position.title
                )
            )
        else:
            messages.success(
                self.request,
                "You have now applied for {}.".format(position.title)
            )
        return super().get(request, *args, **kwargs)


class CancelApplyView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("project",
                       kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        position = get_object_or_404(Position, id=self.kwargs.get("position"))

        try:
            position = Position_Application.objects.get(
                user=self.request.user,
                position=position,
                status=0
            )
        except Position_Application.DoesNotExist:
            messages.warning(
                self.request,
                ("You were already hired for the {} "
                 "position. Too late buddy!").format(
                    position.title
                )
            )
        else:
            position.delete()
            messages.success(
                self.request,
                "You have canceled the application."
            )
        return super().get(request, *args, **kwargs)
