from django.db import models  # This is necessary to define the ULIDField class
import ulid

class ULIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 26
        kwargs['default'] = ulid.new
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)