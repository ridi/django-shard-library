from django.http import HttpResponse
from django.views import View

from shard_static.services import sync_status_monitoring_service


class MonitoringView(View):
    def get(self, request):
        status_data = sync_status_monitoring_service.get_sync_status()
        return HttpResponse(status_data)
