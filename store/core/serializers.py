from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

#***********************************************************************************************************************

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = models.Product
        fields = '__all__'
#***********************************************************************************************************************
class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
    
    def __init__(self, data={}, *args, **kwargs):
        d = []
        for id, count in data.items():
            d.append({'id': id, 'count': count})
        
        # Remove 'many' from kwargs if it exists
        kwargs.pop('many', None)
        super(CartSerializer, self).__init__(data=d, many=True, *args, **kwargs)


    # def to_representation(self, cart_item):
    #


    # def to_internal_value(self, data):
    #     ...

#***********************************************************************************************************************
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


