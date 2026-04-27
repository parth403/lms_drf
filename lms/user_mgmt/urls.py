from django.urls import path
from user_mgmt import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    #authenticaton
    path('api/token/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),
    path('register/',views.RegisterView.as_view(),name='user-register'),
    path('login/',views.LoginView.as_view(),name='user-login'),
    path('logout/',views.LogoutView.as_view(),name='user-logout'),

    #user management
    path('user-detail/',views.UserDetailView.as_view()),
    path('users/',views.UserListViewSet.as_view({'get': 'list'}),name='user-list'),

]
