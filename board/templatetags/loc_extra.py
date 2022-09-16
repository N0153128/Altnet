from django import template
from loc import Me

register = template.Library()


@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None


@register.filter
def random_message(l, i):
    try:
        return Me.greet(i)
    except:
        return None