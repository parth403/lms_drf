from django.shortcuts import render
from rest_framework import viewsets,status
from leave_management.models import LeaveRequest,LeaveLog,LeaveBalance,LeaveType
from .serializers import LeaveRequestSerializer,LeaveLogSerializer,LeaveBalanceSerializer,LeaveRequestCreateSerializer,LeaveTypeSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from leave_management.permissions import IsEmployee,IsManager,IsAdmin
from django.db.models import Q
from rest_framework.response import Response
from lms.common.constants import (ROLE_CHOICES,ROLE_ADMIN,ROLE_EMPLOYEE,ROLE_MANAGER,STATUS_PENDING,STATUS_APPROVED,STATUS_REJECTED,ACTION_APPLIED)
from rest_framework.views import APIView
from .tasks import send_leave_request_email,send_leave_update_email
# Create your views here.

class LeaveRequestCreateView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=LeaveRequestCreateSerializer

    # Create log entry when user request for a leave
    def perform_create(self,serializer):
        leave_request=serializer.save(user=self.request.user,status=STATUS_PENDING)
        LeaveLog.objects.create(leave_request=leave_request,action=ACTION_APPLIED,approved_by=self.request.user)
        send_leave_request_email.delay(leave_request.id)

    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer) 

        # get full details of leave request
        leave_request=LeaveRequest.objects.get(id=serializer.data.get('id'))
        detailed_serializer=LeaveRequestSerializer(leave_request)
        return Response(detailed_serializer.data,status=status.HTTP_201_CREATED)


class EmployeeLeaveRequestListView(generics.ListAPIView):
    #Employee can views their own leave requests
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user).order_by('-applied_at')


class EmployeeLeaveRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user)
    
    def update(self,instance,*args,**kwargs):
        instance=self.get_object()
        if instance.status != STATUS_PENDING:
            return Response({'detail':'Only pending request you can change'},status=status.HTTP_400_BAD_REQUEST)
        return super().update(instance,*args,**kwargs)
        
    def destroy(self,instance,*args,**kwargs):
        instance=self.get_object()
        if instance.status != STATUS_PENDING:
            return Response({'detail':'Only pending request you can delete'},status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(instance,*args,**kwargs)


class PendingLeaveListView(generics.ListAPIView):
    """Manager can view all pendings leaves"""
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated,IsManager]
    
    def get_queryset(self):
        if self.request.user.role!=ROLE_MANAGER:
            return LeaveRequest.objects.none()
        return LeaveRequest.objects.filter(status=STATUS_PENDING).order_by('-applied_at')
    

class LeaveRequestApproveView(APIView):
    permission_classes=[IsAuthenticated]
    
    def patch(self,request,pk):
        if request.user.role!=ROLE_MANAGER:
            return Response({'detail':'ONly manager can approve or reject'},status=status.HTTP_403_FORBIDDEN)
        try:
            leave=LeaveRequest.objects.get(pk=pk)
        except:
            return Response({'detail':'Leave not found'})
        
        if leave.status!=STATUS_PENDING:
            return Response({'detail':'Request alreay approved'})
        
        new_status=request.data.get('status')
        if new_status not in [STATUS_APPROVED,STATUS_REJECTED]:
            return Response({'detail':'status must be approved or rejected'})
        
        leave.status=new_status
        leave.approved_by=request.user
        leave.save()
        send_leave_update_email.delay(leave.id)
        
        LeaveLog.objects.create(leave_request=leave,action=new_status if new_status==STATUS_APPROVED else STATUS_REJECTED,
                                approved_by=request.user)

        serializer=LeaveRequestSerializer(leave)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ManagerLeaveHistoryView(generics.ListAPIView):
    serializer_class=LeaveRequestSerializer
    permission_classes=[IsAuthenticated,IsManager]

    def get_queryset(self):
        return LeaveRequest.objects.all().order_by('-applied_at')


# class LeaveRequestView(generics.RetrieveUpdateDestroyAPIView):
#     queryset=LeaveRequest.objects.all()
#     serializer_class=LeaveRequestSerializer
#     permission_classes=[IsAuthenticated]

class LeaveLogView(generics.ListAPIView):
    serializer_class=LeaveLogSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        qs=LeaveLog.objects.all()
        user_role=self.request.user.role

        if user_role==ROLE_ADMIN:
            return qs
        elif user_role==ROLE_MANAGER:
            filtered=qs.filter(Q(leave_request__user__role=ROLE_EMPLOYEE) | Q(leave_request__user__role=ROLE_MANAGER))
            return filtered
        elif user_role==ROLE_EMPLOYEE:
            return qs.filter(leave_request__user=self.request.user)
        else:
            return qs.none()

# class LeaveUserRequestView(viewsets.ModelViewSet):
#     queryset=LeaveRequest.objects.all()
#     serializer_class=LeaveRequestSerializer

#     def get_serializer_class(self):
#         pass

class LeaveBalanceView(generics.ListAPIView):
    serializer_class=LeaveBalanceSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return LeaveBalance.objects.filter(user=self.request.user)

class LeaveTypeListView(generics.ListAPIView):
    queryset=LeaveType.objects.all()
    serializer_class=LeaveTypeSerializer
    permission_classes=[IsAuthenticated]


