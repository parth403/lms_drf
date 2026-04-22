from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User,LeaveType,LeaveBalance,LeaveRequest,LeaveLog


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token
    
class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    manager_code=serializers.CharField(write_only=True,required=False)

    class Meta:
        model=User
        fields=['id','username','email','role','manager_code','password']

        def create(self,validated_data):
            manager_code=validated_data.pop('manager_code',None)
            role='employee'
            if manager_code=='Manager123':
                role='manager'
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=role
            )
            return user
            
class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveRequest
        fields='__all__'

class LeaveLogSerializer(serializers.ModelSerializer):
    class Meta:
        model=LeaveLog
        fields='__all__'