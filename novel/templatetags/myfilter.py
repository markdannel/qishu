# coding=utf-8


from django import template

register = template.Library()

@register.filter(name='mykey')
def key(d, key):
    return d[int(key)]
