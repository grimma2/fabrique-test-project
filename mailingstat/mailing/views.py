from rest_framework import generics, views
from rest_framework.response import Response

from .models import Mailing
from .serializers import MailingSerializer


class MailingCreateView(generics.CreateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingUpdateView(generics.UpdateAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDeleteView(generics.DestroyAPIView):
    queryset = Mailing.objects.all()


class MailingStatsView(generics.ListAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingDetailStatsView(generics.RetrieveAPIView):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_messages'] = True
        return context