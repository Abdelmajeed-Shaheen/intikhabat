from django.contrib import admin
from .models import (
                        Address,
                        Street,
                        District,
                        Governorate
                    )
# Register your models here.

@admin.register(Address)
class AdminAdress(admin.ModelAdmin):
    list_display=['governorate','street']

@admin.register(Street)
class AdminStreet(admin.ModelAdmin):
    list_display=['name']

@admin.register(District)
class AdminDistrict(admin.ModelAdmin):
    list_display=['name']


@admin.register(Governorate)
class AdminGovernorate(admin.ModelAdmin):
    list_display=['name']