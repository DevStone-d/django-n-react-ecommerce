from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.decorators import login_required


from accounts.models import Account
from panel.models import Discount

from panel.api.serializers import DiscountSerializer

@login_required
@api_view(['GET',])
def api_detail_discount_view(request,code):
    try:
        discount = Discount.objects.get(name=code)
    except Discount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET": 
        serializer = DiscountSerializer(discount)
        return Response(serializer.data)