from rest_framework.permissions import BasePermission
from lms.common.constants import ROLE_ADMIN,ROLE_EMPLOYEE,ROLE_MANAGER

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role==ROLE_EMPLOYEE
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role==ROLE_MANAGER

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.all()