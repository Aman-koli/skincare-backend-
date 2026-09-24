from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import razorpay
from .models import Order, ReturnRequest
from .serializers import OrderSerializer, ReturnRequestSerializer

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "payment_capture": 1,
        })

        order.razorpay_order_id = razorpay_order["id"]
        order.save()

        return Response({
            "order_id": order.id,
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify_payment(self, request):
        payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')
        order_id = request.data.get('order_id')

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            })

            order = Order.objects.get(id=order_id, user=request.user)
            order.payment_id = payment_id
            order.is_paid = True
            order.status = 'placed'
            order.save()

            return Response({"success": True, "message": "Payment verified successfully"})

        except Exception as e:
            return Response({"success": False, "message": "Payment verification failed"}, status=400)


class ReturnRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReturnRequest.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        if order.user != self.request.user:
            raise permissions.PermissionDenied("Not your order")
        serializer.save()