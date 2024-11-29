from django.urls import path
from . import views

urlpatterns = [
    path('extract-contacts/', views.extract_contacts_view, name='extract-contacts'),
]