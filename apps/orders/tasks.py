from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Order Confirmation #{order.id}"
        message = f"Hi {order.customer.username},\n\nYour order has been placed successfully!\nIt will take 3-5 days to be delivered.\n\nThank you for shopping with us!"
        recipient = [order.customer.email]

        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient, fail_silently=False)

        return f"Email sent to {order.customer.email}"
    except Order.DoesNotExist:
        return f"Order {order_id} not found"
