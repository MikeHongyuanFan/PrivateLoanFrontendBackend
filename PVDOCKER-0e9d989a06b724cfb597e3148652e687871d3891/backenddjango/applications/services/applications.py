"""
Application Management Services

This module contains services related to application management,
stage updates, and validation functions.
"""

from json import loads, dumps
from jsonschema import validate, exceptions

from ..models import Application
from documents.models import Note
from users.services import create_application_notification


def update_application_stage(application_id, new_stage, user):
    """
    Update the stage of an application
    
    Args:
        application_id: ID of the application
        new_stage: New stage to set
        user: User making the update
        
    Returns:
        Updated Application object if successful
        
    Raises:
        ValueError: If application not found or invalid stage
    """
    try:
        application = Application.objects.get(id=application_id)
    except Application.DoesNotExist:
        raise ValueError(f"Application with ID {application_id} not found")
    
    # Validate stage
    valid_stages = [choice[0] for choice in Application.STAGE_CHOICES]
    if new_stage not in valid_stages:
        raise ValueError(f"Invalid stage: {new_stage}")
    
    # Store old stage for comparison
    old_stage = application.stage
    
    # Update the stage
    application.stage = new_stage
    application.save()
    
    # Create a note about the stage change
    Note.objects.create(
        application=application,
        title=f"Stage Updated: {old_stage} → {new_stage}",
        content=f"Application stage changed from '{application.get_stage_display()}' to '{application.get_stage_display()}'",
        created_by=user
    )
    
    # Send notifications if needed
    if new_stage in ['approved', 'declined', 'funded']:
        # Notify the broker
        if application.broker and application.broker.user:
            title = f"Application {new_stage.title()}: {application.reference_number}"
            message = f"Application {application.reference_number} has been {new_stage}"
            
            create_application_notification(
                user=application.broker.user,
                title=title,
                message=message,
                application=application,
                notification_type=f'application_{new_stage}'
            )
        
        # Notify borrowers if they have user accounts
        for borrower in application.borrowers.all():
            if hasattr(borrower, 'user') and borrower.user:
                title = f"Application Update: {application.reference_number}"
                message = f"Your loan application has been {new_stage}"
                
                create_application_notification(
                    user=borrower.user,
                    title=title,
                    message=message,
                    application=application,
                    notification_type=f'application_{new_stage}'
                )
    
    return application


def validate_application_schema(application_data):
    """
    Validate application data against a JSON schema
    
    Args:
        application_data: Dictionary containing application data
        
    Returns:
        Tuple of (is_valid, errors)
    """
    # Define the schema for application validation
    schema = {
        "type": "object",
        "properties": {
            "loan_amount": {
                "type": "number",
                "minimum": 1000,
                "maximum": 10000000
            },
            "loan_term": {
                "type": "integer",
                "minimum": 1,
                "maximum": 360
            },
            "interest_rate": {
                "type": "number",
                "minimum": 0,
                "maximum": 50
            },
            "borrowers": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string", "minLength": 1},
                        "last_name": {"type": "string", "minLength": 1},
                        "email": {"type": "string", "format": "email"}
                    },
                    "required": ["first_name", "last_name"]
                }
            },
            "security_properties": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "property_type": {"type": "string"},
                        "current_value": {"type": "number", "minimum": 0}
                    }
                }
            }
        },
        "required": ["loan_amount", "borrowers"]
    }
    
    try:
        validate(instance=application_data, schema=schema)
        return True, []
    except exceptions.ValidationError as e:
        return False, [str(e)]
    except Exception as e:
        return False, [f"Schema validation error: {str(e)}"] 