"""
Simple PDF Field Inspector

This script examines a PDF form and extracts all field names and properties.
"""

import os
import sys
import logging
from pdfrw import PdfReader

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def inspect_pdf_fields(pdf_path):
    """
    Inspect all form fields in a PDF and print their details.
    
    Args:
        pdf_path: Path to the PDF file
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    try:
        logger.info(f"Inspecting PDF: {pdf_path}")
        pdf = PdfReader(pdf_path)
        
        all_fields = {}
        checkbox_fields = {}
        text_fields = {}
        
        # Process each page
        for page_num, page in enumerate(pdf.pages):
            logger.info(f"Examining page {page_num + 1} of {len(pdf.pages)}")
            
            # Check if page has annotations
            if '/Annots' in page:
                annotations = page['/Annots']
                if annotations:
                    logger.info(f"  Found {len(annotations)} annotations on page {page_num + 1}")
                    
                    for i, annotation in enumerate(annotations):
                        if annotation and '/T' in annotation:
                            field_name = str(annotation['/T']).strip('()/')
                            field_type = str(annotation['/FT']).strip('()/') if '/FT' in annotation else "Unknown"
                            field_value = str(annotation['/V']).strip('()/') if '/V' in annotation else "None"
                            field_flags = str(annotation['/Ff']) if '/Ff' in annotation else "None"
                            
                            all_fields[field_name] = {
                                'type': field_type,
                                'value': field_value,
                                'flags': field_flags,
                                'page': page_num + 1
                            }
                            
                            # Categorize fields
                            if field_name.startswith('Check Box'):
                                checkbox_fields[field_name] = all_fields[field_name]
                            elif field_name.startswith('Text'):
                                text_fields[field_name] = all_fields[field_name]
                            
                            # Special focus on employment checkboxes
                            if field_name.startswith('Check Box') and any(str(i) in field_name for i in range(120, 130)):
                                logger.info(f"  EMPLOYMENT CHECKBOX: {field_name} (Type: {field_type}, Value: {field_value})")
        
        # Summary
        logger.info(f"\nFound {len(all_fields)} total form fields:")
        logger.info(f"  - {len(text_fields)} text fields")
        logger.info(f"  - {len(checkbox_fields)} checkbox fields")
        
        # List all checkbox fields
        logger.info("\nAll checkbox fields:")
        for name, props in sorted(checkbox_fields.items()):
            logger.info(f"  {name} (Page: {props['page']}, Type: {props['type']}, Value: {props['value']})")
        
        # Focus on employment checkboxes
        employment_checkboxes = {k: v for k, v in checkbox_fields.items() if any(str(i) in k for i in range(120, 130))}
        logger.info("\nEmployment-related checkboxes (120-130 range):")
        for name, props in sorted(employment_checkboxes.items()):
            logger.info(f"  {name} (Page: {props['page']}, Type: {props['type']}, Value: {props['value']})")
        
        return all_fields
        
    except Exception as e:
        logger.error(f"Error inspecting PDF: {str(e)}")
        return None

if __name__ == "__main__":
    # Path to the application template
    pdf_path = "/Users/hongyuanfan/Desktop/PrivateFundV1/PrivateLoanFrontendBackend/PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/ApplicationTemplate/Eternity Capital - Application Form.pdf"
    
    inspect_pdf_fields(pdf_path)
