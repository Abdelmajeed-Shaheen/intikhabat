from django.contrib import admin
from .models import ComitteeTask
# Register your models here.

@admin.register(ComitteeTask)

class AdminComitteeTask(admin.ModelAdmin):
    list_display=['__str__','is_complete']