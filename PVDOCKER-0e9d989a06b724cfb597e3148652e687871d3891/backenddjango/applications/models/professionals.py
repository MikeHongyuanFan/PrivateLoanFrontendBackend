from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel

class Valuer(BaseModel):
    """Model for storing valuer information."""
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"

    class Meta:
        ordering = ['company_name', 'contact_name']
        verbose_name = _('Valuer')
        verbose_name_plural = _('Valuers')


class QuantitySurveyor(BaseModel):
    """Model for storing quantity surveyor information."""
    company_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.contact_name}"

    class Meta:
        ordering = ['company_name', 'contact_name']
        verbose_name = _('Quantity Surveyor')
        verbose_name_plural = _('Quantity Surveyors')