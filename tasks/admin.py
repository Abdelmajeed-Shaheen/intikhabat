from django.contrib import admin
from .models import ComitteeTask,Comment
# Register your models here.

@admin.register(ComitteeTask)

class AdminComitteeTask(admin.ModelAdmin):
    list_display=['__str__','is_complete']


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):

    list_display=['comment_body','deleted','user','task','timestamp']