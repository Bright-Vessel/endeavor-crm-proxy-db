from django.contrib import admin
from .models import School, AvailabilitySlot, ChildcareCRMToken

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('internal_uuid', 'name', 'crm_id', 'created', 'modified')
    search_fields = ('name', 'crm_id')
    list_filter = ('created', 'modified')
    readonly_fields = ('internal_uuid', 'created', 'modified')
    ordering = ('-created',)

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'end_datetime', 'is_available', 'length', 'school')
    search_fields = ('school__name',)
    list_filter = ('is_available', 'school')
    ordering = ('-start_datetime',)

@admin.register(ChildcareCRMToken)
class ChildcareCRMTokenAdmin(admin.ModelAdmin):
    list_display = ('access_token_short',)
    readonly_fields = ('access_token',)

    def access_token_short(self, obj):
        return obj.access_token[:20] + "..." if obj.access_token else ""
    access_token_short.short_description = 'Access Token (Preview)'
