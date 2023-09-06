from django import template

register = template.Library()


@register.filter
def index(list, index):
    try:
        return list[index]
    except IndexError:
        return None
