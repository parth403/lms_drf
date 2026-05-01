from django.urls import reverse
from rest_framework import status
import pytest
from leave_management.models import LeaveRequest,LeaveType
from user_mgmt.models import User
from lms.conftest import api_client,create_leave_type,employee,manager

@pytest.mark.django_db
class TestLeaveRequest:
    def test_create_authenticated_leave_request(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':employee.id,
            'start_date':'2025-02-02',
            'end_date':'2025-02-05',
            'leave_type':create_leave_type.id,
            'reason':'sick leave'
        },format='json')
        assert response_create.status_code==201

    def test_create_leave_request_with_invalid_data(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
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

    def test_create_leave_request_with_no_data(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':'',
            'start_date':'',
            'end_date':'',
            'leave_type':'',
            'reason':''
        },format='json')
        assert response_create.status_code==400

    def test_create_leave_request_with_end_date_before_start_date(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':1,
            'start_date':'10-02-2024',
            'end_date':'07-02-2024',
            'leave_type':create_leave_type.id,
            'reason':'paid leave'
        },format='json')
        assert response_create.status_code==400

    def test_create_leave_request_with_different_user(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':5,
            'start_date':'10-02-2024',
            'end_date':'07-02-2024',
            'leave_type':create_leave_type.id,
            'reason':'paid leave'
        },format='json')
        print(employee.id)
        assert response_create.status_code==400

    def test_create_leave_request_with_maximum_length_of_reason_field(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':employee.id,
            'start_date':'2022-02-05',
            'end_date':'2022-02-08',
            'leave_type':create_leave_type.id,
            'reason':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Praesentium asperiores voluptatem reiciendis beatae officiis esse, aut minima iusto impedit nemo neque ratione commodi quas delectus velit eos architecto, deleniti amet.'
        },format='json')
        print(response_create)
        assert response_create.status_code==400

    def test_create_leave_request_by_user_cannot_apply_multiple_leaves_with_same_data(self,api_client,employee,create_leave_type):
        api_client.force_authenticate(user=employee)
        url=reverse('leave-request-create')
        response_create=api_client.post(url,data={
            'user':employee.id,
            'start_date':'2025-02-02',
            'end_date':'2025-02-05',
            'leave_type':create_leave_type.id,
            'reason':'sick leave'
        },format='json')
        assert response_create.status_code==201
        assert response_create.data['reason']=='sick leave'