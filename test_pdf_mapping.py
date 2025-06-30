"""
Test script for PDF field mapping and filling.

This script creates a test mapping with employment checkboxes set to various values
and then fills a PDF with these values to test if the checkboxes are properly filled.
"""

import os
import sys
import logging
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def create_test_mapping():
    """Create a test mapping with employment checkboxes set to various values."""
    mapping = {}
    
    # Set text120 (occupation field)
    mapping['text120'] = "Software Engineer"
    
    # Set employment checkboxes - try all formats
    # Format 1: checkbox124 (standard format)
    mapping['checkbox124'] = True  # Full Time
    mapping['checkbox125'] = False  # Part Time
    mapping['checkbox126'] = False  # Casual
    mapping['checkbox127'] = False  # Contract
    
    # Format 2: Check Box124 (PDF format)
    mapping['Check Box124'] = True
    mapping['Check Box125'] = False
    mapping['Check Box126'] = False
    mapping['Check Box127'] = False
    
    # Format 3: Parent IDs
    mapping['parent838'] = True
    mapping['parent835'] = False
    mapping['parent836'] = False
    mapping['parent837'] = False
    
    return mapping

def fill_pdf_with_test_mapping(template_path, output_path):
    """
    Fill PDF form with test mapping data.
    
    Args:
        template_path: Path to the PDF template
        output_path: Path where the filled PDF should be saved
    """
    if not os.path.exists(template_path):
        logger.error(f"Template PDF not found at: {template_path}")
        return
    
    # Create test mapping
    field_mapping = create_test_mapping()
    
    try:
        # Read the template PDF
        template_pdf = PdfReader(template_path)
        
        # Create a new PDF writer
        writer = PdfWriter()
        
        # Process each page
        for page_num, page in enumerate(template_pdf.pages):
            # Get form annotations
            if '/Annots' in page:
                annotations = page['/Annots']
                if annotations:
                    logger.info(f"Page {page_num + 1} has {len(annotations)} annotations")
                    for annotation in annotations:
                        if annotation and '/T' in annotation:
                            field_name = str(annotation['/T']).strip('()/')
                            
                            # Handle text fields (text1, text2, etc.)
                            if field_name.startswith('Text') and field_name[4:].isdigit():
                                field_id = f"text{field_name[4:]}"
                                if field_id in field_mapping:
                                    value = str(field_mapping[field_id])
                                    annotation.update(PdfDict(V=value, AS=value))
                                    logger.info(f"Filling text field {field_name} with value: {value}")
                            
                            # Handle checkbox fields (Check Box20, Check Box21, etc.)
                            elif field_name.startswith('Check Box') and field_name[9:].isdigit():
                                checkbox_num = field_name[9:]
                                field_id = f"checkbox{checkbox_num}"
                                
                                # Extra debugging for employment checkboxes (124-127)
                                if checkbox_num in ['124', '125', '126', '127']:
                                    logger.info(f"EMPLOYMENT CHECKBOX: Processing {field_name} -> {field_id}")
                                    
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
                                    checkbox_value = field_mapping[field_id]
                                    logger.info(f"Checkbox {field_id} value: {checkbox_value}")
                                    if field_mapping[field_id]:
                                        annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                        logger.info(f"Setting checkbox {field_name} to checked")
                                    else:
                                        annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                        logger.info(f"Setting checkbox {field_name} to unchecked")
            
            # Add the page to writer
            writer.addPage(page)
        
        # Special handling for first individual employment checkboxes
        # Based on the PDF inspection, we know the exact coordinates of these checkboxes
        first_individual_employment_checkboxes = [
            {
                'rect': ['27.8182', '410.829', '41.5636', '423.011'],
                'type': 'full_time',
                'field_id': 'checkbox124'
            },
            {
                'rect': ['90.9818', '410.829', '104.727', '423.011'],
                'type': 'part_time',
                'field_id': 'checkbox125'
            },
            {
                'rect': ['155.109', '410.175', '168.854', '422.357'],
                'type': 'casual',
                'field_id': 'checkbox126'
            },
            {
                'rect': ['233.309', '409.52', '247.054', '421.702'],
                'type': 'contract',
                'field_id': 'checkbox127'
            }
        ]
        
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
                            for checkbox in first_individual_employment_checkboxes:
                                # Compare the first two coordinates (top-left corner) with some tolerance
                                if (abs(float(rect_str[0]) - float(checkbox['rect'][0])) < 1 and
                                    abs(float(rect_str[1]) - float(checkbox['rect'][1])) < 1):
                                    
                                    logger.info(f"Found employment checkbox for {checkbox['type']} at {rect_str}")
                                    
                                    # Check if we should check this checkbox
                                    field_id = checkbox['field_id']
                                    if field_id in field_mapping and field_mapping[field_id]:
                                        annotation.update(PdfDict(AS=PdfName.Yes, V=PdfName.Yes))
                                        logger.info(f"Setting {checkbox['type']} checkbox to checked")
                                    else:
                                        annotation.update(PdfDict(AS=PdfName.Off, V=PdfName.Off))
                                        logger.info(f"Setting {checkbox['type']} checkbox to unchecked")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the filled PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"PDF generated successfully at: {output_path}")
        
    except Exception as e:
        logger.error(f"Error filling PDF with mapping: {str(e)}")
        raise

if __name__ == "__main__":
    # Path to the application template
    template_path = "/Users/hongyuanfan/Desktop/PrivateFundV1/PrivateLoanFrontendBackend/PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/ApplicationTemplate/Eternity Capital - Application Form.pdf"
    
    # Path for the output PDF
    output_path = "/Users/hongyuanfan/Desktop/PrivateFundV1/PrivateLoanFrontendBackend/test_output.pdf"
    
    # Fill the PDF with test mapping
    fill_pdf_with_test_mapping(template_path, output_path)
