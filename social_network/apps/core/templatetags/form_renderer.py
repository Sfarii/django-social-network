from django import template
from django.forms.widgets import ClearableFileInput
from django.urls import reverse_lazy

register = template.Library()


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_input_without_label.html')
def form_field_without_label(field, add_ons=None, group_class='mb-3', **kwargs):
    attrs = {**kwargs, 'placeholder': field.label, 'class': kwargs.get('class', '') + ' form-control'}
    return dict(field=field.as_widget(attrs=attrs), help_text=field.help_text, errors=field.errors, add_ons=add_ons,
                group_class=group_class)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_input.html')
def form_field(form_input, **kwargs):
    attrs = {**kwargs, 'class': 'form-control form-control-alternative ' + kwargs.get('class', '')}
    return dict(field=form_input.as_widget(attrs=attrs),
                label=form_input.label_tag(attrs={'class': 'form-control-label'}), errors=form_input.errors)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_start.html')
def form_start(view_name, method='POST', **kwargs):
    return dict(action=reverse_lazy(view_name, kwargs=kwargs), method=method)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_end.html')
def form_end():
    return dict()


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_error.html')
def form_error(form):
    return dict(form=form)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_button.html')
def form_button(button_label, css_class, button_type='submit'):
    return dict(button_label=button_label, button_type=button_type, css_class=css_class)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_avatar_file_input.html')
def avatar_form_field(form_input):
    fn_name = 'file_input_change()'
    attrs = {'class': 'js-file-field-input', 'onchange': fn_name}
    return dict(field=form_input.as_widget(widget=ClearableFileInput(), attrs=attrs),
                context=form_input.field.widget.get_context(name=form_input.name, value=form_input.value, attrs=attrs),
                value=form_input.value, label=form_input.label, input_id=form_input.id_for_label,
                errors=form_input.errors, fn_name=fn_name)


@register.inclusion_tag(filename='templatetags/form_renderer/render_form_file_input.html')
def file_form_field(form_input):
    fn_name = 'file_input_change()'
    attrs = {'class': 'js-file-field-input', 'onchange': fn_name}
    return dict(field=form_input.as_widget(widget=ClearableFileInput(), attrs=attrs),
                context=form_input.field.widget.get_context(name=form_input.name, value=form_input.value, attrs=attrs),
                value=form_input.value, label=form_input.label, input_id=form_input.id_for_label,
                errors=form_input.errors, fn_name=fn_name)
