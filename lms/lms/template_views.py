from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

@require_http_methods(["GET"])
def register_page(request):
    return render(request, 'register.html', {})

@require_http_methods(["GET"])
def login_page(request):
    return render(request, 'login.html', {})

@require_http_methods(['GET'])
def user_dashboard_page(request):
    return render(request,'user_dashboard.html',{})