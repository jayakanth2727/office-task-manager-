from django.contrib import admin
from .models import  Profile, Task, TaskComment

# Register your models here.

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(TaskComment)
