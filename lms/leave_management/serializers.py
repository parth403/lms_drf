from leave_management.models import LeaveType,LeaveBalance,LeaveRequest,LeaveLog
from user_mgmt.models import User
from rest_framework import serializers

# Leave Request Serializer for creating a leave request by employee
class LeaveRequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for leave request'''
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)
    employee_name=serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model=LeaveRequest
        fields=['employee_name','leave_type','leave_type_name','start_date','end_date','reason','applied_at','status','approved_by']
        read_only_fields=['applied_at','approved_by']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Start date should be greater than end date')
        return data
    

    
class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating a leave request 
    '''
    class Meta:
        model=LeaveRequest
        fields='__all__'

class LeaveRequestUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for updating a leave request 
    '''
    class Meta:
        model=LeaveRequest
        fields=['start_date','end_date']

class LeaveRequestApproveSerializer(serializers.ModelSerializer):
    '''
    Serializer for approving and rejecting a leave request by manager
    '''
    class Meta:
        model=LeaveRequest
        fields=['status']

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveType
        fields=('name','max_leaves')

class LeaveBalanceSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.username',read_only=True)
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)

    class Meta:
        model=LeaveBalance
        fields=('user_name','leave_type_name','total_leaves','used_leaves','remaining_leaves')

class LeaveLogSerializer(serializers.ModelSerializer):
    leave_request_name=serializers.CharField(source='leave_request.user.username',read_only=True)
    approved_by_name=serializers.CharField(source='approved_by.username',read_only=True)

    class Meta:
        model=LeaveLog
        fields=['leave_request','leave_request_name','action','approved_by_name']

