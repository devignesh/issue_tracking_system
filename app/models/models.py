from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    """
    User table holds the user basic details.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    dob = models.CharField(max_length=30)
    access_token = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    status = models.BooleanField(default=True)

    def settime(self):
        self.created_at = timezone.now()
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.email


class Project(models.Model):
    """
    Project table holds all the project data
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    languages = models.CharField(max_length=50)
    company_id = models.IntegerField(default=0)


class Issue(models.Model):
    """
    Issue table holds all the issue for the projects
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField()
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # assignee_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee_id = models.IntegerField()
    labels = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Commands(models.Model):
    """
    Commands table holds all the discussions.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField()
    comment = models.CharField(max_length=1000)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
