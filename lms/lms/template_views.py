from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import json
import jwt
from django.conf import settings

@require_http_methods(["GET"])
def register_page(request):
    return render(request, 'register.html', {})

@require_http_methods(["GET"])
def login_page(request):
    token = request.COOKIES.get('access_token')
    if token:
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return redirect('dashboard')
        except:
            pass
    return render(request, 'login.html', {})

@require_http_methods(['GET'])
def user_dashboard_page(request):
    return render(request, 'user_dashboard.html', {})

