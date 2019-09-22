# Create your views here.

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from report.mixins import APILoggingMixin
from .serializer import CalcSerializer
from .utils import calculator


@api_view(['GET'])
@permission_classes([])
def api_root(request, format=None):
    """

    This end point provides the link to calculator api and reports.

    The standard calculator can be used **without authentication**

    The Scientific calculator can be used by authorised(admin) user only. Try logging
    with username **admin** and password is same as **admin@123**.

    """
    return Response({
        'StandardCalculator': reverse('standard-calculator', request=request, format=format),
        'ScientificCalculator': reverse('scientific-calculator', request=request, format=format),
        'APIReport': reverse('api-report-dashboard', request=request, format=format)
    })


class StandardCalculator(APILoggingMixin, APIView):
    """

    This endpoint presents  basic arithmetic operations. The calculator
    can support **add**,**sub**,**mul** and **div**.

    The calculator resource can be accessed by following methods
    The GET /?op=...&a=...&b=... method uses the query parameters to specify the input.

    The POST / method uses a JSON payload of {"op":"string","a":"Number", b":"Number", "op":"string"} to
    specify the input.

    Ex Input : {"op":"add","a":100,"b":200}

    """

    permission_classes = [permissions.AllowAny]

    api_name = 'StandardCalculator'

    def get(self, request):
        data = request.query_params.dict()
        return Response(get_arithmetic_result(data, self.api_name))

    def post(self, request):
        return Response(get_arithmetic_result(request.data, self.api_name))


class ScientificCalculator(APILoggingMixin, APIView):
    """

    This endpoint presents  advanced arithmetic operations. The calculator
    can support **pow**,**fact**,**sqrt**

    The calculator resource can be accessed by following methods
    The GET /?op=...&a=...&b=... method uses the query parameters to specify the input.

    The POST / method uses a JSON payload of {"op":"string","a":"Number", b":"Number", "op":"string"} to
    specify the input.

    Ex Input : {"op":"fact","a":10}

    """
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    api_name = 'ScientificCalculator'

    def get(self, request):
        data = request.query_params.dict()
        return Response(get_arithmetic_result(data, self.api_name))

    def post(self, request):
        return Response(get_arithmetic_result(request.data, self.api_name))


def get_arithmetic_result(input_data, mode):
    serializer = CalcSerializer(data=input_data)
    if mode == 'ScientificCalculator':
        serializer.fields['b'].required = False
    if serializer.is_valid():
        result = calculator(serializer.data['op'], serializer.data['a'], serializer.data.get('b', 0))
    else:
        raise APIException(serializer.errors)
    return result
