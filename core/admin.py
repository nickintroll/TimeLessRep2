from django.contrib import admin
from .models import Parameters

@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
	list_display = ('title', 'value')