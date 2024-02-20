from django.urls import path

from .views import ClientCreateView, ClientUpdateView, ClientDeleteView


urlpatterns = [
    path('add/', ClientCreateView.as_view()),
    path('update/<int:pk>/', ClientUpdateView.as_view()),
    path('delete/<int:pk>/', ClientDeleteView.as_view()),
]

app_name = 'client'