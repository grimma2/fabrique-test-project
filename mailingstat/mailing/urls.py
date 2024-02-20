from django.urls import path

from .views import MailingCreateView, MailingDeleteView, MailingUpdateView, MailingStatsView, MailingDetailStatsView


urlpatterns = [
    path('add/', MailingCreateView.as_view()),
    path('update/<int:pk>', MailingUpdateView.as_view()),
    path('delete/<int:pk>', MailingDeleteView.as_view()),
    path('stats/', MailingStatsView.as_view()),
    path('stats/<int:pk>', MailingDetailStatsView.as_view())
]

app_name = 'mailing'
