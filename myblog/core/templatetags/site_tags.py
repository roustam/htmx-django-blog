from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_site_name():
    return getattr(settings, 'SITE_NAME', "Default Name")