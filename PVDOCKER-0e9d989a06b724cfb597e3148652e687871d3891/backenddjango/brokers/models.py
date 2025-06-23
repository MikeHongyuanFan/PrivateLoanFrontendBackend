from django.db import models
from django.conf import settings


class Branch(models.Model):
    """
    Model for company branches/subsidiaries
    """
    name = models.CharField(max_length=100)
    # DEPRECATED: These fields are kept for data integrity but should not be used in new implementations
    address = models.TextField(null=True, blank=True, help_text="DEPRECATED: Address field is no longer used")
    phone = models.CharField(max_length=20, null=True, blank=True, help_text="DEPRECATED: Phone field is no longer used")
    email = models.EmailField(null=True, blank=True, help_text="DEPRECATED: Email field is no longer used")
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Branch/Subsidiary"
        verbose_name_plural = "Branches/Subsidiaries"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class BDM(models.Model):
    """
    Model for Business Development Managers
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_bdms')
    
    # User relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bdm_profile')
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_bdms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "BDM"
        verbose_name_plural = "BDMs"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Broker(models.Model):
    """
    Model for brokers
    """
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # Relationships
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='branch_brokers')
    bdms = models.ManyToManyField(BDM, related_name='bdm_brokers', blank=True)
    
    # User relationship
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='broker_profile')
    
    # Commission account information
    commission_bank_name = models.CharField(max_length=100, null=True, blank=True)
    commission_account_name = models.CharField(max_length=100, null=True, blank=True)
    commission_account_number = models.CharField(max_length=30, null=True, blank=True)
    commission_bsb = models.CharField(max_length=10, null=True, blank=True)
    
    # Commission account locking
    commission_account_locked = models.BooleanField(default=False, help_text="If True, only super user and accounts can modify commission details")
    commission_account_locked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='locked_commission_accounts')
    commission_account_locked_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_brokers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.company})"
    
    def has_commission_account_data(self):
        """
        Check if broker has any commission account data entered
        """
        return any([
            self.commission_bank_name,
            self.commission_account_name,
            self.commission_account_number,
            self.commission_bsb
        ])
    
    def lock_commission_account(self, user):
        """
        Lock the commission account
        """
        from django.utils import timezone
        self.commission_account_locked = True
        self.commission_account_locked_by = user
        self.commission_account_locked_at = timezone.now()
        self.save()
    
    def unlock_commission_account(self, user):
        """
        Unlock the commission account (only super user or accounts can do this)
        """
        if not user.can_modify_commission_account():
            raise PermissionError("Only super user or accounts can unlock commission accounts")
        
        self.commission_account_locked = False
        self.commission_account_locked_by = None
        self.commission_account_locked_at = None
        self.save()
