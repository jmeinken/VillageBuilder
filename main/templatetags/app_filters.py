from django import template
from datetime import date, timedelta

register = template.Library()





@register.filter(name='label_with_classes', is_safe=True)
def label_with_classes(value, arg):

    return value.label_tag(attrs={'class': arg})


@register.filter(name='remove_colon', is_safe=True)
def remove_colon(value):

    return value.replace(':','')