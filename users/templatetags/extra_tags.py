from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
from django.utils.text import normalize_newlines

register = template.Library()


@register.filter
def no_breaks(text, replacement = ''):
	normalized_text = normalize_newlines(text)
	return mark_safe(normalized_text.replace('\n', replacement))