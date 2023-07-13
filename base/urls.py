from django.urls import path
from .views import read_file, ajax_a2, ajax_a3
urlpatterns = [
    path('', read_file, name="index"),
    path('data_a2/', ajax_a2, name="ajax_a2"),
    path('data_a3/', ajax_a3, name="ajax_a3"),
]
