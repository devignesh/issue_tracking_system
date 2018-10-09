"""issue_tracking_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from django.views.generic.base import TemplateView
from django.conf.urls import handler404, handler500

# App Imports
from app import views
from app.views import LoginView
from app.issues import (
    IssueView,
    IssueDetailsView
)

urlpatterns = [
    path('', views.home, name='home'),

    # Login
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),

    path('users/', views.user, name='user'),
    path('projects/', views.projects, name='projects'),
    # path('comments/', views.comments, name='comments'),

    # get all issue GET
    # create issue POST
    path('issues/', IssueView.as_view(), name='issue'),
    # get issue details by id GET
    # update issue PATCH
    # delete issue DELETE
    path('issue/<int:issue_id>/', IssueDetailsView.as_view(), name='issue_by_id'),

    path('admin/', admin.site.urls),
]

handler404 = views.error_404
handler500 = views.error_500