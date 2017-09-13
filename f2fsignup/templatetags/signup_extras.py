from django import template

register = template.Library()


@register.filter
def has_openings(obj, ministry):
    return obj.has_openings(ministry)
