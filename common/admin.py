from django.contrib import admin
from .models import (
                        Address,
                        Street,
                        District,
                        Governorate,
                        Department,
                        Area,
                        ElectionAddress,
                        Sector,
                        Residence
                    )
# Register your models here.

@admin.register(ElectionAddress)
class AdminElectionAddress(admin.ModelAdmin):
    list_display=['governorate','department']


@admin.register(Address)
class AdminAdress(admin.ModelAdmin):
    list_display=['governorate','street']


@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    list_display=['name','governorate']


@admin.register(Area)
class AdminArea(admin.ModelAdmin):
    list_display=['name','department']

@admin.register(Street)
class AdminStreet(admin.ModelAdmin):
    list_display=['name']

@admin.register(District)
class AdminDistrict(admin.ModelAdmin):
    list_display=['name']


@admin.register(Governorate)
class AdminGovernorate(admin.ModelAdmin):
    list_display=['name']


@admin.register(Sector)
class AdminSector(admin.ModelAdmin):
    list_display=['name']

@admin.register(Residence)
class AdminResidence(admin.ModelAdmin):
    list_display=["governorate","sector","area","district"]