from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from stb.core.models import Profile, Skill, Project, Position, Position_Application
from django.http import Http404
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db import IntegrityError
from django.contrib import messages
import collections
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.forms.formsets import all_valid
from stb.core.forms import UserCreateForm, UserLoginForm, ProfileForm, SkillForm, ProjectForm, PositionForm

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class LoginView(CreateView):
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    template_name = "registration/login.html"


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class Test(TemplateView):
    template_name = "3.html"

class Homepage(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    model = Project

    def get_queryset(self):
        term = self.request.GET.get('q')
        if term:
            projects = Project.objects.filter(
                Q(title__icontains=term) |
                Q(description__icontains=term)
            )
        else:
            projects = Project.objects.all()
        return projects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # profile = Profile.objects.get(user=self.request.user)
        context['projects'] = self.get_queryset()
        context['positions'] = Position.objects.order_by('title').distinct('title')
        return context


class Applications(TemplateView):
    template_name = "applications.html"

    model = Position_Application

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        applicants = Position_Application.objects.all().filter(profile=profile).prefetch_related('user', 'position')
        applicant_dict = {}
        projects = []
        positions = []
        if not self.kwargs:
            for applicant in applicants:
                project_list = []
                project_list.append(applicant.user)
                project_list.append(applicant.position.project)
                project_list.append(applicant.position)
                project_list.append(applicant.status)
                projects.append(applicant.position.project)
                positions.append(applicant.position)
                applicant_dict[applicant.id] = project_list
        elif 'status' in self.kwargs:
            for applicant in applicants:
                project_list = []
                project_list.append(applicant.user)
                project_list.append(applicant.position.project)
                project_list.append(applicant.position)
                project_list.append(applicant.status)
                projects.append(applicant.position.project)
                positions.append(applicant.position)
                applicant_dict[applicant.id] = project_list
                status = self.kwargs.get('status')
                if status == 'accepted':
                    applicant_dict = {k: v for (k, v) in applicant_dict.items() if v[-1] == 1}
                elif status == 'rejected':
                    applicant_dict = {k: v for (k, v) in applicant_dict.items() if v[-1] == 2}
                elif status == 'new-applications':
                    applicant_dict = {k: v for (k, v) in applicant_dict.items() if v[-1] == 0}
                else:
                    raise Http404
        else:
            if 'project' in self.kwargs:
                obj = Project.objects.get(id=self.kwargs.get('project'))
                for applicant in applicants:
                    project_list = []
                    if applicant.position.project.id == obj.id:
                        project_list.append(applicant.user)
                        project_list.append(applicant.position.project)
                        project_list.append(applicant.position)
                        project_list.append(applicant.status)
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
                        project_list.append(applicant.status)
                        applicant_dict[applicant.id] = project_list
                    projects.append(applicant.position.project)
                    positions.append(applicant.position)
        applicant_dict = collections.OrderedDict(sorted(applicant_dict.items()))
        context['applicant_dict'] = applicant_dict


        # Removes duplicates objects based on title
        # Cannot use .distinct() - it is not a QS
        duplicates_dict = {'positions': positions, 'projects': projects}
        seen = collections.OrderedDict()
        for key, value in duplicates_dict.items():
            for obj in value:
                # eliminate this check if you want the last item
                if obj.title not in seen:
                    seen[obj.title] = obj
            context[key] = list(seen.values())
            seen = collections.OrderedDict()

        context['profile'] = profile
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
    form_class = SkillForm
    inlines = [ProfileSkillInline]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'skill_formset'


class ProjectInline(InlineFormSetFactory):
    model = Project
    form_class = ProjectForm
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'project_formset'


class ProfileView(TemplateView):
    template_name = "profile.html"

    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, id=self.kwargs.get('pk'))
        context['skills'] = context['profile'].skills.all()
        context['projects'] = context['profile'].projects.all()
        context['approved_projects'] = Position_Application.objects.filter(user_id=context['profile'].user.id, status=1)
        return context


class ProfileUpdateView(UpdateWithInlinesView):
    model = Profile
    form_class = ProfileForm
    inlines = [ProfileSkillInline, ProjectInline]
    template_name = 'profile_edit.html'

    def get_queryset(self):
        return get_object_or_404(Profile, user=self.request.user, id=self.kwargs.get('pk'))

    def get_object(self, queryset=None):
        return self.get_queryset()


class PositionInline(InlineFormSetFactory):
    model = Position
    form_class = PositionForm
    initial = [{'title': 'Enter Position', 'availability': 'Availability for Applicant'}]
    factory_kwargs = {'extra': 1, 'max_num': None,
                      'can_order': False, 'can_delete': True}
    prefix = 'position_formset'

class CreateProjectView(CreateWithInlinesView):
    model = Project
    form_class = ProjectForm
    inlines = [PositionInline]
    template_name = 'project_new.html'

    def forms_valid(self, form, inlines):
        """
        If the form and formsets are valid, save the associated models.
        """
        self.object.profile = self.request.user.users
        return super().forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ProjectUpdateView(UpdateWithInlinesView):
    model = Project
    form_class = ProjectForm
    inlines = [PositionInline]
    template_name = 'project_edit.html'

    def get_object(self, queryset=None):
        project = get_object_or_404(Project, id=self.kwargs.get('pk'), profile=self.request.user.users.id)
        return project

class ProjectDeleteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("index")

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs.get("pk"))

        if project.profile.user == self.request.user:
            try:
                project.delete()
            except IntegrityError:
                messages.warning(
                    self.request,
                    ("Project {} "
                     "does not exist").format(
                        project.title
                    )
                )
            else:
                messages.warning(
                    self.request,
                    ("Project {} "
                     "succesfully deleted").format(
                        project.title
                    )
                )
        return super().get(request, *args, **kwargs)


class ProjectNeedsView(TemplateView):
    template_name = "index.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        position = Position.objects.get(id=self.kwargs.get('pk'))
        context["position"] = position
        context["projects"] = Project.objects.all().filter(positions__title=position.title)
        context['positions'] = Position.objects.order_by('title').distinct('title')
        return context


class ProjectView(TemplateView):
    template_name = "project.html"

    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(id=self.kwargs.get('pk'))
        context['app_profile'] = Profile.objects.get(id=context['project'].profile.id)
        context['user_profile'] = Profile.objects.get(user=self.request.user)
        positions = context['project'].positions.all()
        applied = {}
        for position in positions:
            position_info=[position]
            applied_applicants = Position_Application.objects.filter(position=position)
            try:
                found = applied_applicants.get(user=self.request.user)
            except:
                try:
                    filled = applied_applicants.get(status=1)
                except:
                    position_info.append(-1)
                    applied[position.id] = position_info
                else:
                    if filled:
                        position_info.append(1)
                        applied[position.id] = position_info
            else:
                if found:
                    position_info.append(found.status)
                    applied[position.id] = position_info


            """
            try:
                found = Position_Application.objects.get(position=position)
                if found.user == self.request.user:
                    position_info.append(found.status)
                    applied[position.id] = position_info
            except:
                position_info.append(-1)
                applied[position.id] = position_info
            """

        context['positions'] = applied
        return context

class ApplyPositionView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("project",
                       kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        position = get_object_or_404(Position, id=self.kwargs.get("position"))
        position_profile = get_object_or_404(Profile, id=position.project.profile_id)

        if position.project.profile.user != self.request.user:
            try:
                obj = Position_Application.objects.get(
                    user=self.request.user,
                    position=position,
                    profile=position_profile,
                )
                if obj.status == 1:
                    messages.success(
                        self.request,
                        "You were hired already for the {} position".format(position.title)
                    )
                if obj.status == 2:
                    messages.success(
                        self.request,
                        "You were rejected already for the {} position".format(position.title)
                    )
                else:
                    messages.warning(
                        self.request,
                        ("You have already applied for {} "
                         "position").format(
                            position.title
                        )
                    )
            except:
                created = Position_Application.objects.create(
                    user=self.request.user,
                    position=position,
                    profile=position_profile,
                    status=0
                )
                if created:
                    messages.success(
                        self.request,
                        "You have now applied for {}.".format(position.title)
                    )
        else:
            messages.warning(
                self.request,
                ("You cannot apply for your own {} "
                 "position").format(
                    position.title
                )
            )
        return super().get(request, *args, **kwargs)


class CancelApplyView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("project",
                       kwargs={"pk": self.kwargs.get("pk")})

    def get(self, request, *args, **kwargs):
        position_main = get_object_or_404(Position, id=self.kwargs.get("position"))
        try:
            position = Position_Application.objects.get(
                user=self.request.user,
                position=position_main,
                profile=position_main.project.profile_id,
            )
        except Position_Application.DoesNotExist:
            messages.warning(
                self.request,
                ("You have never applied for the {} "
                 "position. Maybe you should consider.").format(
                    position_main.title
                )
            )
        else:
            if position.status == 1:
                messages.warning(
                    self.request,
                    ("You were already hired for the {} "
                     "position. Too late buddy!").format(
                        position_main.title
                    )
                )
            elif position.status == 2:
                messages.warning(
                    self.request,
                    ("You were already rejected for the {} "
                     "position. Too late buddy!").format(
                        position_main.title
                    )
                )
            else:
                position.delete()
                messages.success(
                    self.request,
                    "You have canceled the application."
                )
        return super().get(request, *args, **kwargs)


class AcceptProjectProfileView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("applications")

    def get(self, request, *args, **kwargs):

        my_profile = get_object_or_404(Profile, id=self.request.user.users.id)
        profile = get_object_or_404(Profile, id=self.kwargs.get('pk'))
        position = get_object_or_404(Position, id=self.kwargs.get('position'))

        if profile != my_profile:
            applicant = get_object_or_404(Position_Application, position_id=self.kwargs.get('position'), user_id=profile.user.id)
            applicants = Position_Application.objects.filter(position_id=position.id)
            hired = applicants.filter(status=1)

            if hired:
                messages.warning(
                    self.request,
                    ("The {} "
                     "position was already filled").format(
                        position.title
                    )
                )
            else:
                reject_list = []
                for reject in applicants:
                    reject.status = 2
                    reject_list.append(reject)
                Position_Application.objects.bulk_update(reject_list, ['status'])
                applicant.status = 1
                applicant.save()
                messages.success(
                    self.request,
                    "Applicant {} was accepted for the {} position".format(profile.full_name, position.title)
                )

            return super().get(request, *args, **kwargs)
        else:
            messages.warning(
                self.request,
                ("Please do not try to apply to your own projects."))