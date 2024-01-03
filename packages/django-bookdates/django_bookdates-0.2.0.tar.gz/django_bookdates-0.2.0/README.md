# Django Bookdates

A platform for booking dates in shared calendars.

# Installation

Install `django-bookdates` using your favourite package manager.

Add the following to your Django projects `INSTALLED_APPS`:
```
'crispy_forms',
'crispy_bootstrap5',
'django_bookdates'
```

And add the following configuration settings

```
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# If you want to predefine choices for a specific calendar
CALENDAR_CHOICES = { "example-calendar": ['Trixie', 'Liu', 'Enoch'] }
```
