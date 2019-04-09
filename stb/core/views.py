from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from stb.core.models import Profile
from stb.core.forms import UserCreateForm
from django.http import Http404


class Homepage(TemplateView):
    template_name = "index.html"

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


class ProfileEdit(TemplateView):
    template_name = "profile_edit.html"

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"