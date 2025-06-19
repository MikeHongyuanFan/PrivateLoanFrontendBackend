"""
Document models for loan applications.

This module contains models for documents and file management
related to loan applications.
"""

from django.db import models
from django.conf import settings
from .base import TimestampedModel


class Document(TimestampedModel):
    """
    Model for application documents.
    
    Stores files and documents related to loan applications,
    including identification, financial documents, contracts, etc.
    """
    
    # Document type choices
    DOCUMENT_TYPE_CHOICES = [
        ('id', 'Identification'),
        ('income', 'Income Verification'),
        ('bank_statement', 'Bank Statement'),
        ('property', 'Property Document'),
        ('application', 'Application Form'),
        ('contract', 'Contract'),
        ('valuation', 'Valuation Report'),
        ('other', 'Other'),
    ]
    
    # ============================================================================
    # RELATIONSHIPS
    # ============================================================================
    
    application = models.ForeignKey(
        'applications.Application',
        on_delete=models.CASCADE,
        related_name='app_documents',
        null=True,
        blank=True,
        help_text="The application this document belongs to"
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        help_text="User who uploaded this document"
    )
    
    # ============================================================================
    # DOCUMENT DETAILS
    # ============================================================================
    
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other',
        help_text="Type of document"
    )
    file = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        help_text="The uploaded document file"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Additional description of the document"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the document was uploaded"
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['document_type']),
            models.Index(fields=['uploaded_by']),
        ]
    
    def __str__(self):
        """Return a readable representation of the document."""
        doc_type = self.get_document_type_display()
        filename = self.file.name.split('/')[-1] if self.file else "No file"
        return f"{doc_type} - {filename}"
    
    @property
    def filename(self):
        """Get the filename of the uploaded document."""
        return self.file.name.split('/')[-1] if self.file else None
    
    @property
    def file_size(self):
        """Get the file size in bytes."""
        try:
            return self.file.size if self.file else None
        except (ValueError, OSError):
            return None 