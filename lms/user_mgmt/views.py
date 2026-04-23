from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from user_mgmt.serializers import MyTokenObtainPairSerializer,UserSerializer
from user_mgmt.serializers import RegisterSerializer,LoginSerializer
from rest_framework import generics
from user_mgmt.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.db.models import Q
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer


class UserListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        if self.request.user.role == 'Admin':
            qs = qs.all()
        elif self.request.user.role == 'Manager':
            qs = qs.filter(Q(role='Employee') | Q(role='Manager'))
        elif self.request.user.role == 'Employee':
            qs = qs.filter(id=self.request.user.id)
        return qs
    
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[]   

class LoginView(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']

        from rest_framework_simplejwt.tokens import RefreshToken
        refresh=RefreshToken.for_user(user)

        return Response({
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'user':{
                'id':user.id,
                'username':user.username,
                'email':user.email,
                'role':user.role
            }
            },status=status.HTTP_200_OK
        )
