from django.shortcuts import render
from rest_framework import viewsets
from leave_management.models import LeaveRequest,LeaveLog,LeaveBalance
from .serializers import LeaveRequestSerializer,LeaveLogSerializer,LeaveBalanceSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class LeaveRequestCreateView(generics.CreateAPIView):
    queryset=LeaveRequest.objects.all()
    serializer_class=LeaveRequestSerializer

class LeaveRequestView(generics.RetrieveUpdateDestroyAPIView):
    queryset=LeaveRequest.objects.all()
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated]

class LeaveLogView(generics.ListAPIView):
    queryset=LeaveLog.objects.all()
    serializer_class=LeaveLogSerializer
    permission_classes=[IsAuthenticated]

class LeaveBalanceView(generics.ListAPIView):
    queryset=LeaveBalance.objects.all()
    serializer_class=LeaveBalanceSerializer
    permission_classes=[IsAuthenticated]