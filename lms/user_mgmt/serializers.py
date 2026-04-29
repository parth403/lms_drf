#from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user_mgmt.models import User
from leave_management.serializers import LeaveBalanceSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['role'] = user.role
#         return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email','role']
        ordering=['id']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    password_confirm=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=['username','email','password','password_confirm','role','manager']

    def validate(self,data):
        if data['password']!=data['password_confirm']:
            raise serializers.ValidationError('Confirm password not same as password')
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username already exists')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email already exists')
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            manager=validated_data.get('manager')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        model=User
        fields=['username','password']

    def validate(self, attrs):
        username=attrs.get('username')
        password=attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Username and Password Required ')
        
        from django.contrib.auth import authenticate
        user=authenticate(username=username,password=password)

        attrs['user']=user
        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField(required=True)
    def validate(self, attrs):
        self.token=attrs['refresh']
        return attrs
    
    def save(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            RefreshToken(self.token).blacklist()
        except:
            raise serializers.ValidationError('Wrong token')
        
class UserDetailSerializer(serializers.ModelSerializer):
    leave_balances=LeaveBalanceSerializer(source='leavebalance_set',many=True,read_only=True)
    class Meta:
        model=User
        fields=['id','username','email','role','leave_balances']