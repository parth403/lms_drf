from django.db import models
from user_mgmt.models import User
from lms.common.constants import LEAVE_TYPES,STATUS_TYPES,STATUS_PENDING,ACTION_TYPES
# Create your models here.

class LeaveType(models.Model):
    name=models.CharField(max_length=30,choices=LEAVE_TYPES)
    max_leaves=models.IntegerField()

    def __str__(self):
        return self.name

class LeaveBalance(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    leave_type=models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    total_leaves=models.IntegerField()
    used_leaves=models.IntegerField(default=0)

    @property
    def remaining_leaves(self):
        return self.total_leaves - self.used_leaves
    
    def __str__(self):
        return f'{self.user.username} - {self.remaining_leaves} {self.leave_type.name} leaves remaining'
    
class LeaveRequest(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    leave_type=models.ForeignKey(LeaveType,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    reason=models.TextField()
    applied_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=30,choices=STATUS_TYPES,default=STATUS_PENDING)
    approved_by=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL,related_name='leave_approval')

    def __str__(self):
        return f'{self.user.username} - {self.leave_type.name} ({self.start_date} to {self.end_date})'

class LeaveLog(models.Model):
    leave_request=models.ForeignKey(LeaveRequest,on_delete=models.CASCADE)
    action=models.CharField(max_length=30,choices=ACTION_TYPES)
    approved_by=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.approved_by.username} - {self.action}'
    