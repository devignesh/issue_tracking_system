from django.contrib import admin

from app.models import (
    User, 
    Issue,
    Project
)

# Register your models here.

admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Project)
