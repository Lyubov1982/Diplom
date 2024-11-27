# projects/widgets.py
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.html import format_html


class ScrollableCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        return format_html('<div class="scrollable-checkbox-list">{}</div>', output)
