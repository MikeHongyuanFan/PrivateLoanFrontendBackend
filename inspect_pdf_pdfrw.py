"""
PDF Field Inspector using pdfrw

This script examines a PDF form and extracts all field names and properties using pdfrw.
"""

import os
import sys
import logging
from pdfrw import PdfReader

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def inspect_pdf_fields_pdfrw(pdf_path):
    if not os.path.exists(pdf_path):
        logger.error(f"PDF file not found: {pdf_path}")
        return
    try:
        logger.info(f"Inspecting PDF with pdfrw: {pdf_path}")
        pdf = PdfReader(pdf_path)
        fields = []
        for page_num, page in enumerate(pdf.pages):
            if '/Annots' in page:
                for annot in page['/Annots']:
                    if annot and '/T' in annot:
                        field_name = str(annot['/T']).strip('()/')
                        field_type = str(annot['/FT']).strip('()/') if '/FT' in annot else 'Unknown'
                        field_value = str(annot['/V']).strip('()/') if '/V' in annot else 'None'
                        logger.info(f"Page {page_num+1}: {field_name} (Type: {field_type}, Value: {field_value})")
                        fields.append((field_name, field_type, field_value, page_num+1))
        logger.info(f"\nFound {len(fields)} form fields in total.")
        return fields
    except Exception as e:
        logger.error(f"Error inspecting PDF with pdfrw: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    pdf_path = "path/to/your/pdf/template.pdf"
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    inspect_pdf_fields_pdfrw(pdf_path) 