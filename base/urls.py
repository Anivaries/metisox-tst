from django.urls import path
from .views import get_unique_values, get_mean_std, get_percentile_rank
urlpatterns = [
    path('', get_unique_values, name="unique_values"),
    path('data_a_two/', get_mean_std, name="mean_std"),
    path('data_a_three/', get_percentile_rank, name="percentile_rank"),
]
