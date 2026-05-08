from django.contrib import admin
from leave_management.models import *
# Register your models here.

admin.site.register(LeaveType)
admin.site.register(LeaveBalance)
admin.site.register(LeaveRequest)
admin.site.register(LeaveLog)