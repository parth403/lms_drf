import pytest
from django.urls import reverse
from rest_framework import status
from lms.conftest import employee

def test_tokens_with_valid_credentials(client,employee):
    url=reverse('token_obtain_pair')
    data={
        "username":"jenis",
        "password":"jenis123"
    }
    response=client.post(url,data)
    assert response.status_code==200

def test_tokens_with_invalid_credentials(client,employee):
    url=reverse('token_obtain_pair')
    data={
        "username":"dhruvil",
        "password":"dhruvil123"
    }
    response=client.post(url,data)
    assert response.status_code==401

def test_tokens_with_no_data_or_credentials(client,employee):
    url=reverse('token_obtain_pair')
    data={
        "username":"",
        "password":""
    }
    response=client.post(url,data)
    assert response.status_code==400