# templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def times(num):
    return range(num)

@register.filter
def increase_1(num):
    return num+1

@register.filter
def less_10(num):
    return num<10
