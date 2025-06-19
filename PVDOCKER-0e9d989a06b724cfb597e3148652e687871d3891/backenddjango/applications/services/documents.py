"""
Document Services

This module contains services related to document generation, processing,
and signature handling for loan applications.
"""

from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import os
from uuid import uuid4

from ..models import Application
from documents.models import Document


def generate_document(application_id, document_type, user):
    """
    Generate a document for an application
    
    Args:
        application_id: ID of the application
        document_type: Type of document to generate
        user: User generating the document
        
    Returns:
        Document object if successful, None otherwise
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Define template and title based on document type
    template_map = {
        'application_form': {
            'template': 'documents/application_form.html',
            'title': f'Application Form - {application.reference_number}'
        },
        'indicative_letter': {
            'template': 'documents/indicative_letter.html',
            'title': f'Indicative Letter - {application.reference_number}'
        },
        'formal_approval': {
            'template': 'documents/formal_approval.html',
            'title': f'Formal Approval - {application.reference_number}'
        }
    }
    
    if document_type not in template_map:
        return None
    
    template_info = template_map[document_type]
    
    # Generate HTML content
    context = {
        'application': application,
        'borrowers': application.borrowers.all(),
        'guarantors': application.guarantors.all(),
        'broker': application.broker,
        'branch': application.branch,
        'bd': application.bd,
        'generated_date': timezone.now().strftime('%d/%m/%Y'),
    }
    
    html_content = render_to_string(template_info['template'], context)
    
    # Generate PDF - commented out for testing
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_documents', str(application.id))
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{document_type}_{uuid4().hex}.pdf"
    output_path = os.path.join(output_dir, filename)
    
    # Comment out PDF generation for testing
    # HTML(string=html_content).write_pdf(output_path)
    
    # For testing, just create an empty file
    with open(output_path, 'w') as f:
        f.write("Test PDF content")
    
    # Create document record
    relative_path = os.path.join('generated_documents', str(application.id), filename)
    
    document = Document.objects.create(
        title=template_info['title'],
        document_type=document_type,
        file=relative_path,
        file_name=filename,
        file_size=os.path.getsize(output_path),
        file_type='application/pdf',
        application=application,
        created_by=user
    )
    
    return document


def process_signature_data(application_id, signature_data, signed_by, signature_date, user):
    """
    Process signature data for an application
    
    Args:
        application_id: ID of the application
        signature_data: Base64 encoded signature data
        signed_by: Name of the person signing
        signature_date: Date of signature
        user: User processing the signature
        
    Returns:
        Updated Application object if successful, None otherwise
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        return None
    
    # Update application with signature data
    application.signed_by = signed_by
    application.signature_date = signature_date
    application.signature_data = signature_data
    application.save()
    
    # Create a note about the signature
    from documents.models import Note
    Note.objects.create(
        application=application,
        title="Application Signed",
        content=f"Application signed by {signed_by} on {signature_date}",
        created_by=user
    )
    
    # Update application stage if needed
    if application.stage == 'pending_signature':
        application.stage = 'signed'
        application.save()
    
    return application 