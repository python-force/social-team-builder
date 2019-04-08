from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from stb.core.models import Profile
from stb.core.forms import UserCreateForm


class Homepage(TemplateView):
    template_name = "index.html"

class ProfileView(DetailView):
    template_name = "profile.html"
    model = Profile

class ProfileEdit(TemplateView):
    template_name = "profile_edit.html"

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('profile', args=[2])
    template_name = "registration/signup.html"