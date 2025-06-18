# application/templatetags/auth_extras.py
from django import template
from django.contrib.auth.models import Group

register = template.Library()  # Required

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()