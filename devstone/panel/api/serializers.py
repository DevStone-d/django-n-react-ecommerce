from rest_framework import serializers

from panel.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "name",  
            "type_of_discount",
            "discount",
            "created",
            "valid_until",
            "is_valid",
        ]