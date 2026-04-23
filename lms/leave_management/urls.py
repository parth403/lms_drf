
from django.urls import path
from . import views

urlpatterns=[
    path('leave/leave-requests/<int:pk>',views.LeaveRequestView.as_view(),name='leave-request-list'),
    path('leave/leave-request/create/',views.LeaveRequestCreateView.as_view()),
    path('leave/leave-logs/',views.LeaveLogView.as_view()),
    path('leave/leave-balance/',views.LeaveBalanceView.as_view()),

]
