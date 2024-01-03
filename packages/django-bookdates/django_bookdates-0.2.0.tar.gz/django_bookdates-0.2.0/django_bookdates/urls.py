from django.urls import path, include
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="django_bookdates/base.html")),
    path("<str:calendar>/",
         include(
             [
                 path('', views.ListTimespans.as_view(), name='listtimespans'),
                 path('<int:year>-<int:month>-<int:day>', views.ListTimespans.as_view(), name='listtimespans'),
                 path('create', views.CreateTimespan.as_view(), name='createtimespan'),
                 path('delete/<uuid:pk>', views.DeleteTimespan.as_view(), name='deletetimespan'),
                 path('update/<uuid:pk>', views.UpdateTimespan.as_view(), name='updatetimespan'),
                 path('ical', views.Ical.as_view(), name='ical'),
             ]
         )
    ),
]
