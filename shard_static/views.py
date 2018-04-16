from django.shortcuts import render
from django.views import View

from shard_static.services import sync_status_monitoring_service


class MonitoringView(View):
    def get(self, request):
        context = {
            'data': sync_status_monitoring_service.get_sync_status()
        }
        return render(request, 'monitoring.html', context)
