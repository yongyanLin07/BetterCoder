
from django import template
from django.template.defaultfilters import register
from rango.models import Category,Page

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category = None):
    return {'categories':Category.objects.all(),'current_category': current_category}
@register.inclusion_tag('rango/pageDetails.html')
def get_page_list(current_page = None):
    return {'pages':Page.objects.all(),'current_page':current_page}
