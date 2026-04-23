from django.urls import path
from user_mgmt import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns=[
    path('api/token/',views.MyTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),
    path('users/',views.UserListViewSet.as_view({'get': 'list'}),name='user-list'),
    path('user/register/',views.RegisterView.as_view()),
    path('user/login/',views.LoginView.as_view())

]
