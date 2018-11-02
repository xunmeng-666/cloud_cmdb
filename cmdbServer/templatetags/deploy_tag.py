# -*- coding:utf-8-*-
from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_project_name(admin_class):
    return admin_class.model._meta.model_name

@register.simple_tag
def build_project_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name
