from django import template

register = template.Library()


@register.filter
def add_class(field, css_class):
    existing_classes = field.field.widget.attrs.get("class", "")
    classes = f"{existing_classes} {css_class}".strip()
    return field.as_widget(attrs={"class": classes})
