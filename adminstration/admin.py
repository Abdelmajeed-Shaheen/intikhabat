from django.contrib import admin
from .models import (
                     Comittee,
                     ElectionCard,
                     ElectionList
                    )


@admin.register(Comittee)
class AdminComittee(admin.ModelAdmin):
    list_display=['name','manager','is_active','timestamp','updated']


@admin.register(ElectionList)
class AdminElectionList(admin.ModelAdmin):
    list_display=['name','timestamp','updated']


@admin.register(ElectionCard)
class AdminElectionCard(admin.ModelAdmin):
    list_display=['voter','communication_officer']
