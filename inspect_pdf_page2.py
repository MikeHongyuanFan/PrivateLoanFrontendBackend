"""
Simple PDF Field Inspector for Page 2

This script examines page 2 of the PDF form and extracts all field names and properties.
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
        
        # Focus on page 2 (index 1)
        page_num = 1  # 0-based index, so page 2
        page = pdf.pages[page_num]
        
        logger.info(f"Examining page {page_num + 1} of {len(pdf.pages)}")
        
        # Check if page has annotations
        if '/Annots' in page:
            annotations = page['/Annots']
            if annotations:
                logger.info(f"  Found {len(annotations)} annotations on page {page_num + 1}")
                
                # Print all field names on page 2
                logger.info("\nAll fields on page 2:")
                for i, annotation in enumerate(annotations):
                    if annotation and '/T' in annotation:
                        field_name = str(annotation['/T']).strip('()/')
                        field_type = str(annotation['/FT']).strip('()/') if '/FT' in annotation else "Unknown"
                        field_value = str(annotation['/V']).strip('()/') if '/V' in annotation else "None"
                        
                        logger.info(f"  {i+1}. {field_name} (Type: {field_type}, Value: {field_value})")
                        
                        # If this is a checkbox, print more details
                        if field_name.startswith('Check Box'):
                            logger.info(f"     CHECKBOX DETAILS: {field_name}")
                            for key in annotation.keys():
                                logger.info(f"     - {key}: {annotation[key]}")
        
    except Exception as e:
        logger.error(f"Error inspecting PDF: {str(e)}")
        return None

if __name__ == "__main__":
    # Path to the application template
    pdf_path = "/Users/hongyuanfan/Desktop/PrivateFundV1/PrivateLoanFrontendBackend/PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/ApplicationTemplate/Eternity Capital - Application Form.pdf"
    
    inspect_pdf_fields(pdf_path)
