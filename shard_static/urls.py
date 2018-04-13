from django.urls import path

from shard_static.views import MonitoringView

urlpatterns = [
    path('monitoring/', MonitoringView.as_view(), name='monitoring'),
]
