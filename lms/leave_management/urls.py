
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('api/token/',views.MyTokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh_token"),

    path('users/',views.UserListViewSet.as_view({'get': 'list'}),name='user-list'),
    path('leave-requests/<int:pk>',views.LeaveRequestView.as_view(),name='leave-request-list'),
    path('leave-logs/',views.LeaveLogView.as_view())

]
