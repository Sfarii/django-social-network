from django.utils.text import slugify


def generate_unique_slug(model, slug_att_name, slug, title):
    """
    return unique slug if origin slug is exist.
    """
    origin_slug = slug.lower() if slug else slugify(title)
    if slug == origin_slug:
        return origin_slug

    slug = origin_slug
    numb = 1
    while model.objects.filter(**{slug_att_name: slug}).exists():
        slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return slug
