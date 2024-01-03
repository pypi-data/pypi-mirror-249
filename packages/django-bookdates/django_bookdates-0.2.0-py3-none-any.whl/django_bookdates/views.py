from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse

from django_bookdates.models import Timespan
from django_bookdates.forms import TimespanForm

import datetime

from django_bookdates.models import Calendar


class CalendarMixin:
    def dispatch(self, *args, **kwargs):
        if calendar := kwargs.get("calendar"):
            self.calendar = get_object_or_404(Calendar, slug=calendar)
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['calendar'] = self.calendar
        return context


class CreateTimespan(CalendarMixin, CreateView):
    model = Timespan
    form_class = TimespanForm

    def form_valid(self, form, *args, **kwargs):
        timespan = form.save(commit=False)
        timespan.calendar = self.calendar
        timespan.save()
        return super().form_valid(form)

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["calendar"] = self.calendar
        return form_kwargs


class DeleteTimespan(CalendarMixin, DeleteView):
    model = Timespan

    def get_success_url(self):
        return reverse('listtimespans', args=[self.calendar.slug,])


class UpdateTimespan(CalendarMixin, UpdateView):
    model = Timespan
    form_class = TimespanForm

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["calendar"] = self.calendar
        return form_kwargs


class ListTimespans(CalendarMixin, ListView):
    model = Timespan

    def get_queryset(self):
        return Timespan.objects.filter(calendar=self.calendar)

    def get_timespans_on_date(self, date):
        return self.get_queryset().filter(start__lte=date.date(), end__gte=date.date())

    def get_context_data(self, **kwargs):
        today = datetime.datetime.today()
        year = self.kwargs.get('year', today.year)
        month = self.kwargs.get('month', today.month)
        day = self.kwargs.get('day', today.day)
        date = datetime.datetime(year, month, day)

        context = super().get_context_data(**kwargs)
        date = date + datetime.timedelta(days=-date.weekday())
        datelist = [date + datetime.timedelta(days=idx) for idx in range(56)]
        context['weekbefore'] = date + datetime.timedelta(days=-7)
        context['weekafter'] = date + datetime.timedelta(days=7)
        context['fourweeksfromdatedict'] = [{'date': date, 'timespans': self.get_timespans_on_date(date), 'is_today': date.year == today.year and date.month == today.month and date.day == today.day } for date in datelist ]
        context['upcoming'] = self.get_queryset().filter(end__gt=datetime.datetime.today())
        return context


class Ical(CalendarMixin, ListView):
    model = Timespan
    template_name_suffix = "_ical"

    def get_queryset(self):
        return Timespan.objects.filter(calendar=self.calendar)
