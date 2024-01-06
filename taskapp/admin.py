from django.contrib import admin
from taskapp.models import User,Task

class UserAdmin(admin.ModelAdmin):
    list_display=('firstname','lastname','email')
    search_fields=('email',)
class TaskAdmin(admin.ModelAdmin):
    list_display=('title','date_created','status')
    list_filter=('status',)

admin.site.register(User,UserAdmin)
admin.site.register(Task,TaskAdmin)