from django.db.models import CharField


class HashCharField(CharField):
    description = "A hashed field"

    def __init__(self, verbose_name=None, name=None, hasher=None, *args, **kwargs):
        self.hasher = hasher
        super(HashCharField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(HashCharField, self).deconstruct()
        if self.hasher:
            kwargs['hasher'] = self.hasher
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.hasher.decrypt(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.hasher.encrypt(value)

    def get_prep_lookup(self, lookup_type, value):
        # TODO: maybe more lookup type, need to check
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)
