from django import template

from ..models import Profile

register = template.Library()


@register.simple_tag
def user_avatar(user, size=100):
    return user.profile.get_avatar(size)


@register.simple_tag
def user_profile_completion(user):
    completion = 0
    field_list = Profile._meta.get_fields(include_parents=False, include_hidden=False)
    for field in field_list:
        if getattr(user, field.name, None) is not None:
            completion += 1
    return "{:3.2f}".format(completion / len(field_list) * 100)


@register.filter
def is_follower(user, follower):
    return Profile.manager.is_follower(user, follower)


@register.filter
def is_followed(user, followed):
    return Profile.manager.is_followed(user, followed)


