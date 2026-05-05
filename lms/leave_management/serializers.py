from leave_management.models import LeaveType,LeaveBalance,LeaveRequest,LeaveLog
from user_mgmt.models import User
from rest_framework import serializers
from django.db.models import Q

# Leave Request Serializer for creating a leave request by employee
class LeaveRequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for leave request'''
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)
    employee_name=serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model=LeaveRequest
        fields=['id','employee_name','leave_type','leave_type_name','start_date','end_date','reason','applied_at','status','approved_by']
        read_only_fields=['id','applied_at','approved_by']

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date should be less than end date')
        return data
    

    
class LeaveRequestCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating a leave request 
    '''
    class Meta:
        model=LeaveRequest
        fields=['id','leave_type','start_date','end_date','reason']
        read_only_fields=['id']

    def to_internal_value(self, data):
        """Convert camelCase to snake_case and handle field mapping"""
        data = dict(data)        
        camel_to_snake = {
            'leaveType': 'leave_type',
            'startDate': 'start_date',
            'endDate': 'end_date',
        }
        
        for camel, snake in camel_to_snake.items():
            if camel in data:
                data[snake] = data.pop(camel)
        
        return super().to_internal_value(data)

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date should be less than end date')
            
            # Check for overlapping leave requests for the same user
            user = self.context['request'].user
            overlapping_leaves = LeaveRequest.objects.filter(
                user=user,
                start_date__lte=data['end_date'],
                end_date__gte=data['start_date']
            ).exclude(status='rejected')
            
            if overlapping_leaves.exists():
                raise serializers.ValidationError('You already have a leave request for these dates')
        
        return data

class LeaveRequestUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for updating a leave request 
    '''
    class Meta:
        model=LeaveRequest
        fields=['id','start_date','end_date','reason']
        read_only_fields=['id']

    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError('Start date should be less than end date')
        return data

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
        fields=['id','name','max_leaves']

class LeaveBalanceSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.username',read_only=True)
    leave_type_name=serializers.CharField(source='leave_type.name',read_only=True)

    class Meta:
        model=LeaveBalance
        fields=['user_name','leave_type_name','total_leaves','used_leaves','remaining_leaves']

class LeaveLogSerializer(serializers.ModelSerializer):
    leave_request_name=serializers.CharField(source='leave_request.user.username',read_only=True)
    approved_by_name=serializers.CharField(source='approved_by.username',read_only=True)

    class Meta:
        model=LeaveLog
        fields=['leave_request','leave_request_name','action','approved_by_name']

