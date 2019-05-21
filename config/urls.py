"""END URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required

from stb.core.views import (Homepage, SignUp, LoginView, LogoutView, ProfileView,
                            ProfileUpdateView, ProjectView, CreateProjectView,
                            ProjectUpdateView, Applications, ProjectNeedsView,
                            ApplyPositionView, CancelApplyView, AcceptProjectProfileView,
                            ProjectDeleteView, Test)

urlpatterns = [
    path('', Homepage.as_view(), name='index'),
    path('test/', Test.as_view(), name='test'),
    path('profile/<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile-edit'), # Not Tested - PUT not working
    path('profile/<int:pk>/accept/<int:position>/', AcceptProjectProfileView.as_view(), name='applicant-accepted'), # Not Tested
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'), # Tested
    path('project-needs/<int:pk>/', ProjectNeedsView.as_view(), name='project-needs'), # Not Tested
    path('project/<int:pk>/', ProjectView.as_view(), name='project'), # Partially Tested
    path('project/new/', CreateProjectView.as_view(), name='project-new'), # Tested
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'), # Not Tested - PUT not working
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('project/<int:pk>/apply/<int:position>/', ApplyPositionView.as_view(), name='apply-position'), # Tested
    path('project/<int:pk>/cancel-apply/<int:position>/', CancelApplyView.as_view(), name='cancel-apply'), # Tested
    path('applications/', Applications.as_view(), name='applications'),
    path('applications/<str:status>/', Applications.as_view(), name='applications-status'),
    path('applications/project/<int:project>/', Applications.as_view(), name='applications-project'),
    path('applications/position/<int:position>/', Applications.as_view(), name='applications-position'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(), name='logout-user'),
    # path('login/', LoginView.as_view(), name='login'),
    path('accounts/', include('registration.backends.default.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    path('markdownx/', include('markdownx.urls')),
    # re_path(r'^robots\.txt$', include('hide_herokuapp.urls')),
    # re_path(r'^sitemap.xml', 'nautical.views.sitemapxml'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns