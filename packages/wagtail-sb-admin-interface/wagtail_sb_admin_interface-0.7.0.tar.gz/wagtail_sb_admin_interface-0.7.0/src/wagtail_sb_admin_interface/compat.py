# pylint: disable=unused-import, no-name-in-module

import django

if django.VERSION < (2, 0):
    from django.utils.encoding import force_text as force_str
    from django.utils.translation import ugettext_lazy as gettext_lazy
else:
    from django.utils.encoding import force_str
    from django.utils.translation import gettext_lazy
