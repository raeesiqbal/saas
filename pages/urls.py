from django.urls import path
from .views import *


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("records/", RecordsView.as_view(), name="records"),
    path("record-detail/<int:id>", RecordDetailView.as_view(), name="record_detail"),
    path("search/", SearchView.as_view(), name="search"),
]
