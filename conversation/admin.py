from django.contrib import admin
from .models import Scenario

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'difficulty')
    list_filter = ('language', 'difficulty')
    search_fields = ('name',) 
    fields =('name', 'role', 'context', 'language', 'difficulty', 'vocab')