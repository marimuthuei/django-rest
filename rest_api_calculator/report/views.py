from datetime import timedelta

from django.db.models import Count, Avg, Q
from django.utils import timezone
from rest_framework import permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import APIRequestLog

# Create your views here.

available_reports = [1, 7, 30]


class APIReportDashBoard(APIView):
    """

    This end points presents the API metric. This API can be accessed anyone since to know usage of
    basic arithmetic operations API which is public.

    It can also the metrics based on the users if the user is logged in.

    API can be accessed with GET parameter with filter options of 1,7,30

    EX: \?filter = 7

    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        filter_days = self.request.query_params.get('filter', None)
        if filter_days is None:
            raise APIException("please provide valid query parameter.")
        if int(filter_days) not in available_reports:
            raise APIException("please provide the any one (1,7,30) of these numbers ")

        error_count = Count('status_code', filter=Q(status_code__gt=400))

        end_date = timezone.now()
        start_date = end_date - timedelta(days=int(filter_days))
        filtered_requests = APIRequestLog.objects.filter(user=request.user.pk).filter(
            requested_at__range=[start_date, end_date])

        api_report = filtered_requests.values('api_name').annotate(
            request_count=Count('api_name'), median_latency=Avg('latency') / 1000, error_count=error_count)

        return Response(list(api_report))
