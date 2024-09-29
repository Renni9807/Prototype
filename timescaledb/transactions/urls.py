from django.urls import path
from .views import MeasureDataFetchTimeView

urlpatterns = [
    path('measure-data-fetch-time/', MeasureDataFetchTimeView.as_view(), name='measure_data_fetch_time'),
]