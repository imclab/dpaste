from django.template import Library
from dpaste.highlight import pygmentize

register = Library()

@register.filter
def in_list(value, arg):
    return value in arg

@register.filter
def highlight(snippet):
    h = pygmentize(snippet.content, snippet.lexer,
        nbsp=True)
    return h.splitlines()
