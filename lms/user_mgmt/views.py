from django.shortcuts import render
#from rest_framework_simplejwt.views import TokenObtainPairView
from user_mgmt.serializers import UserSerializer,RegisterSerializer,LoginSerializer,LogoutSerializer,UserDetailSerializer
from rest_framework import generics
from user_mgmt.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import viewsets
from django.db.models import Q
from lms.common.constants import ROLE_ADMIN,ROLE_EMPLOYEE,ROLE_MANAGER
# Create your views here.

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class=MyTokenObtainPairSerializer

class UserListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = User.objects.all()
        user_role = self.request.user.role
        
        if user_role == ROLE_ADMIN:
            return qs
        elif user_role == ROLE_MANAGER:
            filtered = qs.filter(Q(role=ROLE_EMPLOYEE) | Q(role=ROLE_MANAGER))
            return filtered
        elif user_role == ROLE_EMPLOYEE:
            return qs.filter(id=self.request.user.id)
        else:
            return qs.none()
    
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

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
    
class LogoutView(APIView):
    permission_classes=[]
    def post(self,request):
        serializer=LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Logout Successfully'})
    
class UserDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request):
        serializer=UserDetailSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)


