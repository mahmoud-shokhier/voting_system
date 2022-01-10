from django.contrib import admin
from .models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model= Choice

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('id', 'name', 'description','expiry_date_time' )
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_filter = ('name',)
# Register your models here.
admin.site.register(Poll, PollAdmin)
