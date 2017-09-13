from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def has_openings(obj, ministry):
    return obj.has_openings(ministry)
