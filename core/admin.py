from django.contrib import admin
from .models import Parameters, Text, TextBlock

@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
	list_display = ('title', 'value')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
	list_display = ('block', 'language', 'text')
	search_fields = ('text', )

@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
	list_display = ('title', )