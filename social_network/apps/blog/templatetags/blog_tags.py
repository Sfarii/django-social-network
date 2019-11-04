from django import template

register = template.Library()


@register.simple_tag
def is_liked_by(likes, user, return_if_true=True, return_if_false=False):
    for like in likes:
        if like.author == user:
            return return_if_true
    return return_if_false
