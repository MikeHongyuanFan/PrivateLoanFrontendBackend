from rest_framework import permissions


class IsSuperUserOrAccounts(permissions.BasePermission):
    """
    Permission to only allow super user or accounts users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['super_user', 'accounts']


class IsAdmin(permissions.BasePermission):
    """
    Permission to only allow admin users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'


class IsAdminOrBroker(permissions.BasePermission):
    """
    Permission to only allow admin or broker users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'broker']


class IsAdminOrBD(permissions.BasePermission):
    """
    Permission to only allow admin or BD users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'bd']


class IsAdminOrBrokerOrBD(permissions.BasePermission):
    """
    Permission to only allow admin, broker, or BD users
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['admin', 'broker', 'bd']


class CanModifyCommissionAccount(permissions.BasePermission):
    """
    Permission to modify commission account details
    Only super user and accounts can modify commission accounts
    """
    def has_permission(self, request, view):
        if not request.user:
            return False
        
        # Super user and accounts can always modify
        if request.user.can_modify_commission_account():
            return True
        
        # For other users, check if this is a create operation (first time entry)
        if request.method == 'POST':
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        
        # Super user and accounts can always modify
        if request.user.can_modify_commission_account():
            return True
        
        # For other users, check if commission account is locked
        if hasattr(obj, 'commission_account_locked') and obj.commission_account_locked:
            return False
        
        # If commission account has data and is not locked, only super user/accounts can modify
        if hasattr(obj, 'has_commission_account_data') and obj.has_commission_account_data():
            return False
        
        return True


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to only allow owners of an object or admin users
    """
    def has_object_permission(self, request, view, obj):
        # Super user and accounts can do anything
        if request.user.role in ['super_user', 'accounts']:
            return True
        
        # Admin can do anything (except commission account modifications)
        if request.user.role == 'admin':
            return True
        
        # Check if object has a user field
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if object has a created_by field
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False


class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission to only allow users to access their own details or admin users to access any user details
    """
    def has_permission(self, request, view):
        # Super user and accounts can do anything
        if request.user and request.user.role in ['super_user', 'accounts']:
            return True
        
        # Admin can do anything
        if request.user and request.user.role == 'admin':
            return True
            
        # For retrieve action, check if the user is requesting their own details
        if view.action == 'retrieve':
            return True
            
        # For other actions, deny access to non-admin users
        return False
        
    def has_object_permission(self, request, view, obj):
        # Super user and accounts can do anything
        if request.user.role in ['super_user', 'accounts']:
            return True
        
        # Admin can do anything
        if request.user.role == 'admin':
            return True
            
        # Users can only access their own details
        return obj.id == request.user.id


class CanAccessNote(permissions.BasePermission):
    """
    Permission to check if a user can access a note
    """
    def has_permission(self, request, view):
        # All authenticated users can access the view
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Super user and accounts can access any note
        if user.role in ['super_user', 'accounts']:
            return True
        
        # Admin can access any note
        if user.role == 'admin':
            return True
        
        # Check if the user is the creator of the note
        if hasattr(obj, 'created_by') and obj.created_by == user:
            return True
        
        # Check if the user is assigned to the note
        if hasattr(obj, 'assigned_to') and obj.assigned_to == user:
            return True
        
        # Check if the user is the broker associated with the application
        if hasattr(obj, 'application') and obj.application and hasattr(obj.application, 'broker'):
            if obj.application.broker and hasattr(obj.application.broker, 'user'):
                if obj.application.broker.user == user:
                    return True
        
        # Check if the user is the BD associated with the application
        if hasattr(obj, 'application') and obj.application and hasattr(obj.application, 'bd'):
            if obj.application.bd == user:
                return True
        
        # Check if the user is a borrower associated with the application or note
        if user.role == 'client' and hasattr(user, 'borrower_profile'):
            # Check if the note is directly associated with the borrower
            if hasattr(obj, 'borrower') and obj.borrower == user.borrower_profile:
                return True
            
            # Check if the note is associated with an application that includes the borrower
            if hasattr(obj, 'application') and obj.application:
                if user.borrower_profile in obj.application.borrowers.all():
                    return True
        
        return False