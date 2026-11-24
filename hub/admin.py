from django.contrib import admin
from .models import Club, Event, JoinRequest


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'tagline', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'date', 'location')
    list_filter = ('club',)
    search_fields = ('title',)


@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'club', 'submitted_at')
    list_filter = ('club',)
    search_fields = ('name', 'email')
    readonly_fields = ('submitted_at',)
