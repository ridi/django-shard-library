from django.shortcuts import render
from django.views import View

from shard_static.services import transmit_status_monitoring_service


class MonitoringView(View):
    def get(self, request):
        context = {
            'data': transmit_status_monitoring_service.get_transmit_status()
        }
        return render(request, 'monitoring.html', context)
