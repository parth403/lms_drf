from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer
from rest_framework import viewsets
from .models import User,LeaveRequest,LeaveLog
from .serializers import UserSerializer,LeaveRequestSerializer,LeaveLogSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser,IsAuthenticated
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer

class UserListViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role=='Admin':
            qs = qs.all()
        elif self.request.user.role=='Manager':
            qs = qs.filter(role='Employee')
        elif self.request.user.role=='Employee':
            qs = qs.filter(id=self.request.user.id)
        return qs

class LeaveRequestView(generics.RetrieveUpdateDestroyAPIView):
    queryset=LeaveRequest.objects.all()
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated]

class LeaveLogView(generics.ListAPIView):
    queryset=LeaveLog.objects.all()
    serializer_class=LeaveLogSerializer
    permission_classes=[IsAuthenticated]