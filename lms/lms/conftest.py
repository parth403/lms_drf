import pytest
from rest_framework.test import APIClient
from user_mgmt.models import User
from leave_management.models import LeaveType

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="jenis",
        email="jenis@example.com",
        password="jenis123"
    )

@pytest.fixture
def create_leave_type(db):
    return LeaveType.objects.create(name='paid',max_leaves=10)


@pytest.fixture
def api_client():
    return APIClient()