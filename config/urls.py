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

from stb.core.views import (Homepage, SignUp, ProfileView,
                            ProfileUpdateView, ProjectView, CreateProjectView,
                            ProjectUpdateView, Applications)

urlpatterns = [
    path('', Homepage.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project'),
    path('project/new/', CreateProjectView.as_view(), name='project-new'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project-edit'),
    path('applications/', Applications.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
    # re_path(r'^robots\.txt$', include('hide_herokuapp.urls')),
    # re_path(r'^sitemap.xml', 'nautical.views.sitemapxml'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns