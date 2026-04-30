from django.urls import reverse
from rest_framework import status
import pytest
from leave_management.models import LeaveRequest,LeaveType
from user_mgmt.models import User
from lms.conftest import user,api_client,create_leave_type

@pytest.mark.django_db
class TestLeaveRequest:
    def test_create_authenticated_leave_request(self,api_client,user,create_leave_type):
        api_client.force_authenticate(user=user)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':user.id,
            'start_date':'2025-02-02',
            'end_date':'2025-02-05',
            'leave_type':create_leave_type.id,
            'reason':'sick leave'
        },format='json')
        assert response_create.status_code==201

    def test_create_leave_request_with_invalid_data(self,api_client,user,create_leave_type):
        api_client.force_authenticate(user=user)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':1,
            'start_date':'02-02-2025',
            'end_date':'01-02-2025',
            'leave_type':create_leave_type.id,
            'reason':'sick leave'
        },format='json')
        assert response_create.status_code==400

    def test_create_leave_request_unauthenticated(self,api_client,create_leave_type):
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':1,
            'start_date':'02-02-2025',
            'end_date':'01-02-2025',
            'leave_type':create_leave_type.id,
            'reason':'sick leave'
        },format='json')
        assert response_create.status_code==401