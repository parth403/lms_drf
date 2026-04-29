
from django.urls import path
from . import views

urlpatterns=[
    #path('leave-request/<int:pk>',views.LeaveRequestView.as_view(),name='leave-request-list'),

    #leave-logs
    path('leave-logs/',views.LeaveLogView.as_view(),name='leave-logs'),

    #leave-balance
    path('leave-balance/',views.LeaveBalanceView.as_view(),name='leave-balance'),

    #leave-type
    path('leave-types/',views.LeaveTypeListView.as_view(),name='leave-type'),

    #leave-request Employee
    path('leave-request-create/',views.LeaveRequestCreateView.as_view(),name='leave-requesr-create'),
    path('my-leaves/',views.EmployeeLeaveRequestListView.as_view(),name='my-all-requests'),
    path('my-leaves/<int:pk>',views.EmployeeLeaveRequestDetailView.as_view(),name='my-leave-requests'),

    #manager leaves
    path('pending-leaves/',views.PendingLeaveListView.as_view()),
    path('leave-request-approve/<int:pk>',views.LeaveRequestApproveView.as_view()),
    path('all-leave-request',views.ManagerLeaveHistoryView.as_view()),


]
