from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BookingRequest, Equipment, EquipmentCategory, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("ConstructLink", {'fields': ('account_type',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("ConstructLink", {'fields': ('account_type',)}),)
    list_display = ('username', 'email', 'account_type', 'is_staff')


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner', 'region', 'district', 'daily_price', 'availability_status')
    list_filter = ('category', 'availability_status', 'region')
    search_fields = ('name', 'description', 'region', 'district')


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'requested_by', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('equipment__name', 'requested_by__username', 'site_location')
