from rest_framework import serializers
from leave_management.models import LeaveType,LeaveBalance,LeaveRequest,LeaveLog


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveRequest
        fields='__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('Start date should be greater than end date')
        return data
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class LeaveLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveLog
        fields='__all__'

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveBalance
        fields=('user','leave_type','total_leaves','used_leaves','remaining_leaves')

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveType
        fields=('name','max_leaves')