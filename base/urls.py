from django.urls import path
from .views import read_file, data_a_two, data_a_three
urlpatterns = [
    path('', read_file, name="index"),
    path('data_a_two/', data_a_two, name="data_a_two"),
    path('data_a_three/', data_a_three, name="data_a_three"),
]
