"""
PDF Field Inspector using fitz (PyMuPDF)

This script examines a PDF form and extracts all field names and properties
using the fitz library to understand why checkboxes 124-127 are not being filled.
"""

import os
import sys
import logging
import fitz  # PyMuPDF

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def inspect_pdf_fields_fitz(pdf_path):
    """
    Inspect all form fields in a PDF using fitz and print their details.
    
    Args:
        pdf_path: Path to the PDF file
    """
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return
    
    try:
        logger.info(f"Inspecting PDF with fitz: {pdf_path}")
        doc = fitz.open(pdf_path)
        all_fields = {}
        checkbox_fields = {}
        text_fields = {}
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            annots = page.annots()
            if annots is None:
                continue
            logger.info(f"Page {page_num + 1}: Found {len(list(annots))} annotations")
            for annot in annots:
                if annot.type[0] == fitz.PDF_ANNOT_WIDGET:
                    field_name = annot.field_name
                    field_type = annot.field_type
                    field_value = annot.field_value
                    all_fields[field_name] = {
                        'type': field_type,
                        'value': field_value,
                        'page': page_num + 1,
                        'rect': annot.rect,
                    }
                    if field_name and field_name.startswith('Check Box'):
                        checkbox_fields[field_name] = all_fields[field_name]
                    elif field_name and field_name.startswith('Text'):
                        text_fields[field_name] = all_fields[field_name]
                    # Special focus on employment checkboxes
                    if field_name and field_name.startswith('Check Box') and any(str(i) in field_name for i in range(120, 130)):
                        logger.info(f"EMPLOYMENT CHECKBOX: {field_name} (Type: {field_type}, Value: {field_value}, Page: {page_num+1})")
                        logger.info(f"  Rect: {annot.rect}")
        logger.info(f"\nFound {len(all_fields)} total form fields:")
        logger.info(f"  - {len(text_fields)} text fields")
        logger.info(f"  - {len(checkbox_fields)} checkbox fields")
        logger.info("\nAll checkbox fields:")
        for name, props in sorted(checkbox_fields.items()):
            logger.info(f"  {name} (Page: {props['page']}, Type: {props['type']}, Value: {props['value']})")
        employment_checkboxes = {k: v for k, v in checkbox_fields.items() if any(str(i) in k for i in range(120, 130))}
        logger.info("\nEmployment-related checkboxes (120-130 range):")
        for name, props in sorted(employment_checkboxes.items()):
            logger.info(f"  {name} (Page: {props['page']}, Type: {props['type']}, Value: {props['value']})")
        doc.close()
        return all_fields
    except Exception as e:
        logger.error(f"Error inspecting PDF with fitz: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_checkbox_filling_fitz(template_path, output_path):
    """
    Test filling checkboxes 124-127 using fitz to see if they can be filled.
    """
    try:
        logger.info(f"Testing checkbox filling with fitz")
        logger.info(f"Template: {template_path}")
        logger.info(f"Output: {output_path}")
        doc = fitz.open(template_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            annots = page.annots()
            if annots is None:
                continue
            for annot in annots:
                if annot.type[0] == fitz.PDF_ANNOT_WIDGET:
                    field_name = annot.field_name
                    if field_name and field_name.startswith('Check Box') and field_name[9:] in ['124', '125', '126', '127']:
                        should_check = field_name == 'Check Box124'  # Only 124 checked for test
                        logger.info(f"Setting {field_name} to {'checked' if should_check else 'unchecked'}")
                        try:
                            annot.set_widget_value("Yes" if should_check else "Off")
                        except Exception as e:
                            logger.error(f"Error setting {field_name}: {str(e)}")
        doc.save(output_path)
        doc.close()
        logger.info(f"Test PDF saved to {output_path}")
    except Exception as e:
        logger.error(f"Error testing checkbox filling: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    pdf_path = "path/to/your/pdf/template.pdf"
    output_path = "path/to/output/test_filled.pdf"
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    fields = inspect_pdf_fields_fitz(pdf_path)
    test_checkbox_filling_fitz(pdf_path, output_path) 