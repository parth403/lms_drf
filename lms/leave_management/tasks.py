from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from leave_management.models import LeaveRequest
from lms.common.constants import (ROLE_MANAGER)
from user_mgmt.models import User
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_leave_request_email(leave_request_id):
    leave = LeaveRequest.objects.get(id=leave_request_id)

    manager = leave.user.manager

    if manager and manager.email:
        send_mail(
            subject='New Leave Request',
            message=f'{leave.user.username} applied for leave from {leave.start_date} to {leave.end_date}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[manager.email],
            fail_silently=False
        )
        
@shared_task
def send_leave_update_email(leave_request_id):
    leave=LeaveRequest.objects.get(id=leave_request_id)
    user=leave.user
    if user and user.email:
        send_mail(
            subject='Confirmation for the applied leave',
            message=f'Your leave from {leave.start_date} to {leave.end_date} has been approved',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[leave.user.email],
            fail_silently=False
        )