from django import template

register = template.Library()


@register.inclusion_tag(filename='templatetags/pagination_renderer/pagination.html')
def paginator_render(page_obj):
    current_page = page_obj.number
    paginator = page_obj.paginator
    return dict(current_page=current_page, paginator=paginator)