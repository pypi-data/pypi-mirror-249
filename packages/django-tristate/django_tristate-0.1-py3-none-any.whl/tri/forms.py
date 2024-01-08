from django import forms
from django.utils.safestring import mark_safe

class TriStateWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.CheckboxInput(),
            forms.CheckboxInput()
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value is None:
            return [False, False]
        return [value, not value]

    def format_output(self, rendered_widgets):
        # This method is optional and can be used for custom rendering
        return mark_safe(u''.join(rendered_widgets))

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Remove the 'required' attribute from the subwidgets
        for subwidget in context['widget']['subwidgets']:
            subwidget['attrs'].pop('required', None)
        return context


class TriStateField(forms.MultiValueField):
    widget = TriStateWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.BooleanField(required=False),
            forms.BooleanField(required=False)
        )
        # Ensure the field itself is not required
        kwargs['required'] = False
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            yes, no = data_list
            if yes and not no:
                return True
            elif no and not yes:
                return False
            else:
                return None
        return None

