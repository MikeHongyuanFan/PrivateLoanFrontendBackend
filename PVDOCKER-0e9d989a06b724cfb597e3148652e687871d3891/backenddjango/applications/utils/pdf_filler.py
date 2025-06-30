"""
PDF Form Filler Utility

This module contains functions to fill PDF forms with application data.
"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime, date
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from django.conf import settings
from .pdf_field_mapping import generate_pdf_field_mapping_from_json

logger = logging.getLogger(__name__)


def fill_pdf_form(application, output_path: str) -> List[str]:
    """
    Fill a PDF form with application data using the correct field mapping.
    
    Args:
        application: The Application instance
        output_path: Path where the filled PDF should be saved
    
    Returns:
        List of missing fields that couldn't be filled
    """
    try:
        # Get the cascade data for the application
        from ..serializers.application import ApplicationDetailSerializer
        from rest_framework.test import APIRequestFactory
        
        # Create a mock request for the serializer
        factory = APIRequestFactory()
        request = factory.get('/')
        
        # Serialize the application with cascade data
        serializer = ApplicationDetailSerializer(application, context={'request': request})
        cascade_data = serializer.data
        
        # Generate the PDF field mapping using our tested utility
        field_mapping = generate_pdf_field_mapping_from_json(cascade_data)
        
        # Log the mapping for debugging
        logger.info(f"Generated PDF field mapping with {len(field_mapping)} fields")
        logger.debug(f"Field mapping: {field_mapping}")
        
        # Get the template PDF path
        template_path = get_pdf_template_path()
        
        # Fill the PDF using the field mapping
        missing_fields = fill_pdf_with_mapping(template_path, field_mapping, output_path)
        
        logger.info(f"PDF form filled successfully: {output_path}")
        return missing_fields
        
    except Exception as e:
        logger.error(f"Error filling PDF form: {str(e)}")
        raise


def fill_pdf_with_mapping(template_path: str, field_mapping: Dict[str, Any], output_path: str) -> List[str]:
    """
    Fill PDF form with field mapping data using pdfrw library.
    
    Args:
        template_path: Path to the PDF template
        field_mapping: Dictionary mapping field IDs to values
        output_path: Path where the filled PDF should be saved
    
    Returns:
        List of missing fields that couldn't be filled
    """
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template PDF not found at: {template_path}")
    
    try:
        # Read the template PDF
        template_pdf = PdfReader(template_path)
        
        # Create a new PDF writer
        writer = PdfWriter()
        
        missing_fields = []
        all_checkbox_fields = []  # Collect all checkbox field names
        
        # Process each page
        for page_num, page in enumerate(template_pdf.pages):
            # Get form annotations
            if '/Annots' in page:
                annotations = page['/Annots']
                if annotations:
                    logger.debug(f"Page {page_num + 1} has {len(annotations)} annotations")
                    for annotation in annotations:
                        if annotation and '/T' in annotation:
                            field_name = str(annotation['/T']).strip('()/')
                            
                            # Log all field names to see the exact format
                            if field_name.startswith('Check Box'):
                                all_checkbox_fields.append(field_name)
                                logger.debug(f"Found checkbox field: '{field_name}'")
                            
                            # Handle text fields (text1, text2, etc.)
                            if field_name.startswith('Text') and field_name[4:].isdigit():
                                field_id = f"text{field_name[4:]}"
                                if field_id in field_mapping:
                                    value = str(field_mapping[field_id])
                                    annotation.update(PdfDict(V=value, AS=value))
                                    logger.debug(f"Filling text field {field_name} with value: {value}")
                                else:
                                    logger.debug(f"Missing text field data for {field_id} -> {field_name}")
                                    missing_fields.append(field_id)
                            
                            # Handle checkbox fields (Check Box20, Check Box21, etc.)
                            elif field_name.startswith('Check Box') and field_name[9:].isdigit():
                                checkbox_num = field_name[9:]
                                field_id = f"checkbox{checkbox_num}"
                                
                                # Extra debugging for employment checkboxes (124-127)
                                if checkbox_num in ['124', '125', '126', '127']:
                                    logger.info(f"EMPLOYMENT CHECKBOX: Processing {field_name} -> {field_id}")
                                    logger.info(f"EMPLOYMENT CHECKBOX: Raw field name from PDF: '{field_name}'")
                                    logger.info(f"EMPLOYMENT CHECKBOX: Extracted number: '{checkbox_num}'")
                                    logger.info(f"EMPLOYMENT CHECKBOX: Mapped field ID: '{field_id}'")
                                    
                                    # Check for parent ID in the annotation
                                    parent_id = None
                                    if '/Parent' in annotation:
                                        parent_id = str(annotation['/Parent']).strip('()/').split(',')[0]
                                        logger.info(f"EMPLOYMENT CHECKBOX: Parent ID: {parent_id}")
                                        
                                        # Try to map using parent ID
                                        parent_field_id = f"parent{parent_id}"
                                        if parent_field_id in field_mapping:
                                            logger.info(f"EMPLOYMENT CHECKBOX: Found mapping by parent ID: {parent_field_id} = {field_mapping[parent_field_id]}")
                                            if field_mapping[parent_field_id]:
                                                annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                                logger.info(f"EMPLOYMENT CHECKBOX: Setting checkbox {field_name} to checked via parent ID")
                                            else:
                                                annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                                logger.info(f"EMPLOYMENT CHECKBOX: Setting checkbox {field_name} to unchecked via parent ID")
                                            continue
                                    
                                    # Try direct field name mapping
                                    if field_name in field_mapping:
                                        logger.info(f"EMPLOYMENT CHECKBOX: Found mapping by exact name: {field_name} = {field_mapping[field_name]}")
                                        if field_mapping[field_name]:
                                            annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                            logger.info(f"EMPLOYMENT CHECKBOX: Setting checkbox {field_name} to checked via exact name")
                                        else:
                                            annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                            logger.info(f"EMPLOYMENT CHECKBOX: Setting checkbox {field_name} to unchecked via exact name")
                                        continue
                                    
                                    if field_id in field_mapping:
                                        logger.info(f"EMPLOYMENT CHECKBOX: Value in mapping: {field_mapping[field_id]}")
                                    else:
                                        logger.info(f"EMPLOYMENT CHECKBOX: NOT FOUND IN MAPPING!")
                                        # Try alternative formats
                                        alt_formats = [
                                            f"checkbox{int(checkbox_num)}",  # Without leading zeros
                                            f"checkbox{checkbox_num.zfill(3)}",  # With leading zeros
                                            f"checkbox{checkbox_num.lstrip('0')}",  # Strip leading zeros
                                            f"Check Box{checkbox_num}",  # Original PDF format
                                            f"Check Box {checkbox_num}"  # With space
                                        ]
                                        logger.info(f"EMPLOYMENT CHECKBOX: Trying alternative formats: {alt_formats}")
                                        for alt_format in alt_formats:
                                            if alt_format in field_mapping:
                                                logger.info(f"EMPLOYMENT CHECKBOX: Found in alternative format: {alt_format} = {field_mapping[alt_format]}")
                                
                                logger.debug(f"Processing checkbox field: {field_name} -> {field_id}")
                                if field_id in field_mapping:
                                    checkbox_value = field_mapping[field_id]
                                    logger.debug(f"Checkbox {field_id} value: {checkbox_value} (type: {type(checkbox_value)})")
                                    if field_mapping[field_id]:
                                        annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                        logger.debug(f"Setting checkbox {field_name} to checked")
                                    else:
                                        annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                        logger.debug(f"Setting checkbox {field_name} to unchecked")
                                else:
                                    logger.debug(f"Checkbox {field_id} not found in field mapping")
                                    logger.debug(f"Missing checkbox data for {field_id} -> {field_name}")
                                    missing_fields.append(field_id)
            
            # Add the page to writer
            writer.addPage(page)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the filled PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Log all checkbox fields found in the template
        logger.info(f"All checkbox fields found in PDF template: {sorted(all_checkbox_fields)}")
        
        # Look for employment-related checkboxes (around 120-130 range)
        employment_checkboxes = [field for field in all_checkbox_fields if any(str(i) in field for i in range(120, 131))]
        logger.info(f"Employment-related checkboxes (120-130 range): {sorted(employment_checkboxes)}")
        
        # Look for checkboxes that might be for first individual (around 100-130 range)
        first_individual_checkboxes = [field for field in all_checkbox_fields if any(str(i) in field for i in range(100, 131))]
        logger.info(f"Potential first individual checkboxes (100-130 range): {sorted(first_individual_checkboxes)}")
        
        # Look for checkboxes that might be for employment types (any range)
        employment_keywords = ['full', 'part', 'casual', 'contract', 'employment', 'work']
        potential_employment_checkboxes = []
        for field in all_checkbox_fields:
            # Check if any employment-related keywords might be in the field name
            # Since we can't see the actual field names, let's look for patterns
            if any(keyword in field.lower() for keyword in employment_keywords):
                potential_employment_checkboxes.append(field)
        logger.info(f"Potential employment checkboxes (by keywords): {sorted(potential_employment_checkboxes)}")
        
        # Comprehensive analysis of checkbox field numbers
        checkbox_numbers = []
        for field in all_checkbox_fields:
            try:
                # Extract the number from "Check Box123" -> 123
                number = int(field.replace('Check Box', ''))
                checkbox_numbers.append(number)
            except:
                pass
        
        checkbox_numbers.sort()
        logger.info(f"All checkbox numbers found: {checkbox_numbers}")
        
        # Look for patterns - checkboxes that might be in groups of 4 (like employment types)
        potential_groups = []
        for i in range(len(checkbox_numbers) - 3):
            group = checkbox_numbers[i:i+4]
            if len(group) == 4 and all(group[j+1] - group[j] == 1 for j in range(3)):
                potential_groups.append(group)
        
        logger.info(f"Potential checkbox groups of 4 consecutive numbers: {potential_groups}")
        
        # Special handling for first individual employment checkboxes
        # Use the coordinates provided in the mapping
        if 'employment_checkboxes' in field_mapping:
            employment_checkboxes = field_mapping['employment_checkboxes']
            
            # Process each page again to find these specific checkboxes by coordinates
            logger.info("=== SPECIAL HANDLING FOR EMPLOYMENT CHECKBOXES ===")
            for page_num, page in enumerate(template_pdf.pages):
                if '/Annots' in page:
                    annotations = page['/Annots']
                    if annotations:
                        for annotation in annotations:
                            if annotation and '/Rect' in annotation and '/Subtype' in annotation and annotation['/Subtype'] == '/Widget':
                                rect = annotation['/Rect']
                                rect_str = [str(r).strip('()') for r in rect]
                                
                                # Check if this annotation matches any of our employment checkboxes
                                for checkbox in employment_checkboxes:
                                    # Compare the first two coordinates (top-left corner) with some tolerance
                                    if (abs(float(rect_str[0]) - float(checkbox['rect'][0])) < 1 and
                                        abs(float(rect_str[1]) - float(checkbox['rect'][1])) < 1):
                                        
                                        logger.info(f"Found employment checkbox for {checkbox['type']} at {rect_str}")
                                        
                                        # Check if we should check this checkbox
                                        if checkbox['value']:
                                            annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                            logger.info(f"Setting {checkbox['type']} checkbox to checked")
                                        else:
                                            annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                            logger.info(f"Setting {checkbox['type']} checkbox to unchecked")
        
        # Special debug for employment checkboxes
        logger.info("=== EMPLOYMENT CHECKBOX DEBUG ===")
        for i in range(120, 130):
            checkbox_id = f"checkbox{i}"
            if checkbox_id in field_mapping:
                logger.info(f"{checkbox_id} = {field_mapping[checkbox_id]}")
            else:
                logger.info(f"{checkbox_id} = NOT IN MAPPING")
        
        # Check if there are any checkboxes with similar numbers in different formats
        all_keys = list(field_mapping.keys())
        employment_related = [k for k in all_keys if any(f"checkbox{i}" in k.lower() for i in range(120, 130))]
        logger.info(f"All employment-related keys in mapping: {employment_related}")
        
        # Check the actual PDF field names for these checkboxes
        logger.info("=== PDF FIELD NAMES FOR EMPLOYMENT CHECKBOXES ===")
        employment_checkbox_fields = [field for field in all_checkbox_fields if any(str(i) in field for i in range(120, 130))]
        logger.info(f"Employment checkbox fields in PDF: {sorted(employment_checkbox_fields)}")
        
        logger.info(f"PDF generated successfully at: {output_path}")
        return missing_fields
        
    except Exception as e:
        logger.error(f"Error filling PDF with mapping: {str(e)}")
        raise


def get_pdf_template_path(template_name: str = 'default_template') -> str:
    """
    Get the path to a PDF template.
    
    Args:
        template_name: Name of the template
    
    Returns:
        Path to the PDF template file
    """
    # Try multiple possible template locations
    possible_paths = [
        os.path.join(settings.BASE_DIR, 'templates', 'pdf', f"{template_name}.pdf"),
        os.path.join(settings.BASE_DIR, 'applications', 'ApplicationTemplate', 'Eternity Capital - Application Form.pdf'),
        os.path.join(settings.BASE_DIR, 'applications', 'templates', f"{template_name}.pdf"),
        os.path.join(settings.BASE_DIR, 'static', 'pdf', f"{template_name}.pdf"),
    ]
    
    for template_path in possible_paths:
        if os.path.exists(template_path):
            return template_path
    
    # If no template found, raise error with all attempted paths
    raise FileNotFoundError(f"PDF template not found. Tried paths: {possible_paths}")


def validate_pdf_fields(field_mapping: Dict[str, Any]) -> List[str]:
    """
    Validate that required PDF fields are present in the mapping.
    
    Args:
        field_mapping: Dictionary mapping field IDs to values
    
    Returns:
        List of missing required fields
    """
    # Define required fields based on the PDF specification
    required_fields = [
        'text1',  # Company Name (if company borrower)
        'text106',  # Title (if individual borrower)
        'text107',  # Given Names (if individual borrower)
        'text108',  # Surname (if individual borrower)
        'text297',  # Net Loan Required
        'text298',  # Term Required
    ]
    
    missing_fields = []
    for field_id in required_fields:
        if field_id not in field_mapping or not field_mapping[field_id]:
            missing_fields.append(field_id)
    
    return missing_fields


def get_field_mapping_summary(field_mapping: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of the field mapping for debugging and validation.
    
    Args:
        field_mapping: Dictionary mapping field IDs to values
    
    Returns:
        Summary dictionary with counts and sample data
    """
    text_fields = {k: v for k, v in field_mapping.items() if k.startswith('text')}
    checkbox_fields = {k: v for k, v in field_mapping.items() if k.startswith('checkbox')}
    
    return {
        'total_fields': len(field_mapping),
        'text_fields_count': len(text_fields),
        'checkbox_fields_count': len(checkbox_fields),
        'filled_text_fields': len([v for v in text_fields.values() if v]),
        'checked_checkboxes': len([v for v in checkbox_fields.values() if v]),
        'sample_text_fields': dict(list(text_fields.items())[:5]),
        'sample_checkbox_fields': dict(list(checkbox_fields.items())[:5]),
    } 