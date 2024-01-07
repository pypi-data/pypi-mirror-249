![Community-Project](https://gitlab.com/softbutterfly/open-source/open-source-office/-/raw/master/banners/softbutterfly-open-source--banner--community-project.png)

![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/wagtail-sb-admin-interface)
![PyPI - Package version](https://img.shields.io/pypi/v/wagtail-sb-admin-interface)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wagtail-sb-admin-interface)
![PyPI - MIT License](https://img.shields.io/pypi/l/wagtail-sb-admin-interface)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f28072e8e0ac4605bd3235b7643929ad)](https://app.codacy.com/gl/softbutterfly/wagtail-sb-admin-interface/dashboard?utm_source=gl&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

# Wagtail Admin Interface

Customize the Wagtail admin interface from the admin itself.

Inspired by [django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface).

## Requirements

- Python 3.9.0 or higher
- Django 4.0.0 or higher
- Wagtail 4.0.0 or higher

## Install

```bash
pip install wagtail-sb-admin-interface
```

## Usage

Add `wagtail.contrib.settings`, `wagtail.contrib.modeladmin`, `colorfield` and `wagtail_sb_admin_interface` to your `INSTALLED_APPS` settings

```
INSTALLED_APPS = [
  "wagtail_sb_admin_interface",
  # ...
  "wagtail.contrib.settings",
  "wagtail.contrib.modeladmin",
  "colorfield",
  # ...
]
```

## Docs

- [Ejemplos](https://gitlab.com/softbutterfly/open-source/wagtail-sb-admin-interface/-/wikis)
- [Wiki](https://gitlab.com/softbutterfly/open-source/wagtail-sb-admin-interface/-/wikis)

## Changelog

All changes to versions of this library are listed in the [change history](CHANGELOG.md).

## Development

Check out our [contribution guide](CONTRIBUTING.md).

## Contributors

See the list of contributors [here](https://gitlab.com/softbutterfly/open-source/wagtail-sb-admin-interface/-/graphs/develop).
