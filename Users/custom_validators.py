import functools
import gzip
import os
import re
from django.utils.translation import ngettext  # https://docs.python.org/2/library/gettext.html#gettext.ngettext
from django.core.exceptions import ValidationError
from difflib import SequenceMatcher
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
class MyCustomMinimumLengthValidator(object):
        def __init__(self, min_length=8):  # put default min_length here
            self.min_length = min_length

        def validate(self, password, user=None):
            if len(password) < self.min_length:
                raise ValidationError(
                    ngettext(
                        # silly, I know, but if your min length is one, put your message here
                        "A password é demasiado pequena.Deverá conter pelo menos %(min_length)d caracteres",
                        # if it's more than one (which it probably is) put your message here
                       "A password é demasiado pequena.Deverá conter pelo menos %(min_length)d caracteres",
                        self.min_length
                    ),
                code='password_too_short',
                params={'min_length': self.min_length},
                )

        def get_help_text(self):
            return ngettext(
                # you can also change the help text to whatever you want for use in the templates (password.help_text)
                "A password deverá conter pelo menos %(min_length)d caracteres",
                "A password deverá conter pelo menos %(min_length)d caracteres",
                self.min_length
            ) % {'min_length': self.min_length}


class MyUserAttributeSimilarityValidator:
    """
    Validate whether the password is sufficiently different from the user's
    attributes.

    If no specific attributes are provided, look at a sensible list of
    defaults. Attributes that don't exist are ignored. Comparison is made to
    not only the full attribute value, but also its components, so that, for
    example, a password is validated against either part of an email address,
    as well as the full address.
    """
    DEFAULT_USER_ATTRIBUTES = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = re.split(r'\W+', value) + [value]
            for value_part in value_parts:
                if SequenceMatcher(a=password.lower(), b=value_part.lower()).quick_ratio() >= self.max_similarity:
                    try:
                        verbose_name = str(user._meta.get_field(attribute_name).verbose_name)
                    except FieldDoesNotExist:
                        verbose_name = attribute_name
                    raise ValidationError(
                        ("A password é demasiado semelhante ao %(verbose_name)s."),
                        code='password_too_similar',
                        params={'verbose_name': verbose_name},
                    )

    def get_help_text(self):
        return ("A password não pode ser demasiado semelhante aos restantes dados.")


class MyNumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                ("Esta password é inteiramente numérica."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return ("A password não pode ser inteiramente numérica.")