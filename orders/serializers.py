from rest_framework import serializers
from .models import Order, OrderItem, ReturnRequest

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'price', 'quantity']


class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = ['id', 'order', 'reason', 'description', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    return_requests = ReturnRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'full_name', 'phone', 'address', 'city', 'state', 'pincode',
            'total_amount', 'status', 'is_paid', 'items', 'return_requests', 'created_at'
        ]
        read_only_fields = ['status', 'is_paid', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order