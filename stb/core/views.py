from django.views.generic import TemplateView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from stb.core.models import Profile, Skill, Project, Position, Position_Application
from stb.core.forms import UserCreateForm
from django.http import Http404
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.views.generic import RedirectView
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib import messages
import collections
from django.http import HttpResponseRedirect
from django.forms.formsets import all_valid

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class Test(TemplateView):
    template_name = "3.html"

class Homepage(TemplateView):
    template_name = "index.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = Profile.objects.get(user=self.request.user)
        projects = Project.objects.all()
        context['projects'] = projects
        #context['positions'] = Position.objects.all().order_by('title')
        context['positions'] = Position.objects.order_by('title').distinct('title')
        return context


class Applications(TemplateView):
    template_name = "applications.html"

    model = Position_Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = Profile.objects.get(user=self.request.user)
        applicants = Position_Application.objects.all().prefetch_related('user', 'position')
        applicant_dict = {}
        projects = []
        positions = []
        if not self.kwargs:
            for applicant in applicants:
                project_list = []
                project_list.append(applicant.user)
                project_list.append(applicant.position.project)
                project_list.append(applicant.position)
                projects.append(applicant.position.project)
                positions.append(applicant.position)
                applicant_dict[applicant.id] = project_list
        else:
            if 'project' in self.kwargs:
                obj = Project.objects.get(id=self.kwargs.get('project'))
                for applicant in applicants:
                    project_list = []
                    if applicant.position.project.id == obj.id:
                        project_list.append(applicant.user)
                        project_list.append(applicant.position.project)
                        project_list.append(applicant.position)
                        applicant_dict[applicant.id] = project_list
                    projects.append(applicant.position.project)
                    positions.append(applicant.position)
            elif 'position' in self.kwargs:
                obj = Position.objects.get(id=self.kwargs.get('position'))
                for applicant in applicants:
                    project_list = []
                    if applicant.position.title == obj.title:
                        project_list.append(applicant.user)
                        project_list.append(applicant.position.project)
                        project_list.append(applicant.position)
                        applicant_dict[applicant.id] = project_list
                    projects.append(applicant.position.project)
                    positions.append(applicant.position)
        context['applicant_dict'] = applicant_dict
        context['projects'] = projects

        # Removes duplicates objects based on title
        # Cannot use .distinct() - it is not a QS
        seen = collections.OrderedDict()
        for obj in positions:
            # eliminate this check if you want the last item
            if obj.title not in seen:
                seen[obj.title] = obj

        context['positions'] = list(seen.values())
        return context


"""
class ApplicationsProjectView(TemplateView):
    template_name = "applications.html"

    model = Position_Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applicants = Position_Application.objects.all().prefetch_related('user', 'position')
        applicant_dict = {}
        projects = []
        for applicant in applicants:
            project_list = []
            project_list.append(applicant.user)
            project_list.append(applicant.position.project)
            project_list.append(applicant.position)
            projects.append(applicant.position.project)
            applicant_dict[applicant.id] = project_list
        context['applicant_dict'] = applicant_dict
        context['projects'] = projects
        position = Position.objects.get(id=self.kwargs.get('pk'))
        context["projects"] = Project.objects.all().filter(positions__title=position.title)
        return context
"""


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
        profile = get_object_or_404(Profile, user=self.request.user, id=self.kwargs.get('pk'))
        context['profile'] = profile
        context['skills'] = profile.skills.all()
        context['projects'] = profile.projects.all()
        return context


class ProfileUpdateView(UpdateWithInlinesView):
    model = Profile
    inlines = [ProfileSkillInline, ProjectInline]
    fields = ['full_name', 'description', 'avatar']
    template_name = 'profile_edit.html'

    def get_queryset(self):
        return get_object_or_404(Profile, user=self.request.user, id=self.kwargs.get('pk'))

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
