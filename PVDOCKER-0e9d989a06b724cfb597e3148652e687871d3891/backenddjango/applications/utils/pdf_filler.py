import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from django.conf import settings
from ..models import Application
from .pdf_constants import FIELD_MAP, CHECKBOX_MAP, PDF_CONFIG, ERROR_MESSAGES, SUCCESS_MESSAGES

logger = logging.getLogger(__name__)


class PDFFormFiller:
    """
    Main PDF form filler class that handles filling PDF forms with application data.
    
    This class provides methods to:
    1. Extract application data and map it to PDF form fields
    2. Fill PDF forms with the extracted data
    3. Handle errors and validation
    """
    
    def __init__(self, application: Application):
        """
        Initialize the PDF form filler with an application instance.
        
        Args:
            application: The Application model instance to extract data from
        """
        self.application = application
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def fill_form(self, output_path: str) -> List[str]:
        """
        Fill PDF form with application data.
        
        Args:
            output_path: Path where the filled PDF should be saved
            
        Returns:
            List of error messages, empty if successful
        """
        try:
            return fill_pdf_form(self.application, output_path)
        except Exception as e:
            self.logger.error(f"Error filling PDF form: {str(e)}")
            return [f"Error filling PDF form: {str(e)}"]
    
    def extract_data(self) -> Dict[str, Any]:
        """
        Extract application data for PDF form filling.
        
        Returns:
            Dictionary containing application data mapped to PDF field names
        """
        try:
            return extract_application_data(self.application)
        except Exception as e:
            self.logger.error(f"Error extracting application data: {str(e)}")
            return {}
    
    def extract_checkbox_data(self) -> Dict[str, bool]:
        """
        Extract checkbox data from application.
        
        Returns:
            Dictionary containing checkbox states mapped to PDF checkbox field names
        """
        try:
            return extract_checkbox_data(self.application)
        except Exception as e:
            self.logger.error(f"Error extracting checkbox data: {str(e)}")
            return {}


def fill_pdf_form(application: Application, output_path: str) -> List[str]:
    """
    Fill a PDF form with application data.
    
    Args:
        application: Application instance containing the data
        output_path: Path where the filled PDF should be saved
        
    Returns:
        List of error messages, empty if successful
    """
    errors = []
    
    try:
        # Get the PDF template path
        template_path = os.path.join(
            settings.BASE_DIR, 
            'applications', 
            'ApplicationTemplate', 
            'Loan Application Form.pdf'
        )
        
        if not os.path.exists(template_path):
            error_msg = f"{ERROR_MESSAGES['pdf_not_found']}: {template_path}"
            logger.error(error_msg)
            return [error_msg]
        
        # Read the PDF template
        try:
            reader = PdfReader(template_path)
        except Exception as e:
            error_msg = f"{ERROR_MESSAGES['pdf_read_error']}: {str(e)}"
            logger.error(error_msg)
            return [error_msg]
        
        # Extract application data
        try:
            text_data = extract_application_data(application)
            checkbox_data = extract_checkbox_data(application)
        except Exception as e:
            error_msg = f"{ERROR_MESSAGES['invalid_application']}: {str(e)}"
            logger.error(error_msg)
            return [error_msg]
        
        # Combine all data
        all_data = {**text_data, **checkbox_data}
        
        # Log data mapping for debugging
        logger.info(f"Filling PDF for application {application.id} with {len(all_data)} fields")
        
        # Fill the form fields
        filled_fields = 0
        skipped_fields = 0
        
        for page in reader.pages:
            if '/Annots' in page:
                for annotation in page['/Annots']:
                    if annotation is None:
                        continue
                    
                    annotation = annotation.getObject()
                    
                    if '/Subtype' in annotation and annotation['/Subtype'] == '/Widget':
                        if '/T' in annotation:
                            field_name = annotation['/T']
                            
                            # Remove parentheses from field name if present
                            if field_name.startswith('(') and field_name.endswith(')'):
                                field_name = field_name[1:-1]
                            
                            # Find corresponding data key
                            data_key = None
                            for key, pdf_field in FIELD_MAP.items():
                                if pdf_field == field_name:
                                    data_key = key
                                    break
                            
                            # Check checkbox mapping if not found in text fields
                            if not data_key:
                                for key, pdf_field in CHECKBOX_MAP.items():
                                    if pdf_field == field_name:
                                        data_key = key
                                        break
                            
                            # Fill the field if we have data
                            if data_key and data_key in all_data:
                                value = all_data[data_key]
                                
                                # Handle different field types
                                if isinstance(value, bool):
                                    # Checkbox field
                                    if value:
                                        annotation.update(PdfDict(V=PdfName.Yes, AS=PdfName.Yes))
                                    else:
                                        annotation.update(PdfDict(V=PdfName.Off, AS=PdfName.Off))
                                else:
                                    # Text field
                                    annotation.update(PdfDict(V=str(value)))
                                
                                filled_fields += 1
                                logger.debug(f"Filled field {field_name} ({data_key}) with value: {value}")
                            else:
                                skipped_fields += 1
                                if data_key:
                                    logger.debug(f"No data for field {field_name} ({data_key})")
                                else:
                                    logger.debug(f"Unknown field: {field_name}")
        
        logger.info(f"PDF filling completed: {filled_fields} fields filled, {skipped_fields} fields skipped")
        
        # Write the filled PDF
        try:
            writer = PdfWriter()
            writer.trailer = reader.trailer
            writer.pages = reader.pages
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            writer.write(output_path)
            
            logger.info(f"{SUCCESS_MESSAGES['pdf_generated']}: {output_path}")
            
        except Exception as e:
            error_msg = f"{ERROR_MESSAGES['pdf_write_error']}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
        
    except Exception as e:
        error_msg = f"Unexpected error during PDF generation: {str(e)}"
        logger.error(error_msg)
        errors.append(error_msg)
    
    return errors


def extract_application_data(application: Application) -> Dict[str, Any]:
    """
    Extract data from Application model and related models for PDF form filling
    Based on corrected field mappings
    """
    data = {}
    
    # Basic loan details
    if application.loan_amount:
        data["loan_amount"] = str(application.loan_amount)
    if application.loan_term:
        data["loan_term"] = str(application.loan_term)
    if application.interest_rate:
        data["expected_rate"] = str(application.interest_rate)
    
    # Settlement date
    if application.estimated_settlement_date:
        settlement_date = application.estimated_settlement_date
        data["settlement_date_day"] = str(settlement_date.day)
        data["settlement_date_month"] = str(settlement_date.month)
        data["settlement_date_year"] = str(settlement_date.year)
    
    # Additional comments
    if application.additional_comments:
        data["additional_comments"] = application.additional_comments
    
    # Get company borrowers
    company_borrowers = application.borrowers.filter(is_company=True)
    if company_borrowers.exists():
        company = company_borrowers.first()
        
        # Basic company info
        if company.company_name:
            data["company_name"] = company.company_name
        if company.company_abn:
            data["company_abn_acn"] = company.company_abn
        elif company.company_acn:
            data["company_abn_acn"] = company.company_acn
        if company.industry_type:
            data["company_industry_type"] = company.industry_type.title()
        if company.contact_number:
            data["company_contact_number"] = company.contact_number
        if company.annual_company_income:
            data["annual_company_income"] = str(company.annual_company_income)
        if company.trustee_name:
            data["trustee_name"] = company.trustee_name
        
        # Company address
        if company.registered_address_unit:
            data["company_address_unit"] = company.registered_address_unit
        if company.registered_address_street_no:
            data["company_address_street_no"] = company.registered_address_street_no
        if company.registered_address_street_name:
            data["company_address_street_name"] = company.registered_address_street_name
        if company.registered_address_suburb:
            data["company_address_suburb"] = company.registered_address_suburb
        if company.registered_address_state:
            data["company_address_state"] = company.registered_address_state
        if company.registered_address_postcode:
            data["company_address_postcode"] = company.registered_address_postcode
        
        # Directors (if available)
        directors = company.directors.all()
        if directors.exists():
            director1 = directors[0] if len(directors) >= 1 else None
            director2 = directors[1] if len(directors) >= 2 else None
            
            if director1:
                data["director1_name"] = director1.name
                if director1.director_id:
                    # Split director ID into individual digits (up to 12 characters)
                    director_id = str(director1.director_id).ljust(12, ' ')
                    for i in range(12):
                        if i < len(director_id) and director_id[i] != ' ':
                            data[f"director1_id_{i+1}"] = director_id[i]
            
            if director2:
                data["director2_name"] = director2.name
                if director2.director_id:
                    # Split director ID into individual digits (up to 12 characters)
                    director_id = str(director2.director_id).ljust(12, ' ')
                    for i in range(12):
                        if i < len(director_id) and director_id[i] != ' ':
                            data[f"director2_id_{i+1}"] = director_id[i]
    
    # Get individual borrowers (up to 2)
    individual_borrowers = application.borrowers.filter(is_company=False)
    borrower_count = 0
    
    for borrower in individual_borrowers[:2]:  # Limit to 2 borrowers
        borrower_count += 1
        prefix = f"borrower{borrower_count}"
        
        # Basic individual info
        if borrower.first_name:
            data[f"{prefix}_given_names"] = borrower.first_name
        if borrower.last_name:
            data[f"{prefix}_surname"] = borrower.last_name
        
        # Date of birth
        if borrower.date_of_birth:
            dob = borrower.date_of_birth
            data[f"{prefix}_dob_day"] = str(dob.day)
            data[f"{prefix}_dob_month"] = str(dob.month)
            data[f"{prefix}_dob_year"] = str(dob.year)
        
        # Contact info
        if borrower.phone:
            data[f"{prefix}_phone"] = borrower.phone
        if borrower.email:
            data[f"{prefix}_email"] = borrower.email
        
        # Address (parse from residential_address)
        if borrower.residential_address:
            # Try to extract components from full address
            address_parts = borrower.residential_address.split(',')
            if len(address_parts) >= 2:
                street_part = address_parts[0].strip()
                # Try to extract unit and street number from street part
                street_words = street_part.split()
                if len(street_words) >= 2:
                    # First word might be unit, second might be street number
                    if street_words[0].lower().startswith(('unit', 'apt', 'level')):
                        data[f"{prefix}_address_unit"] = street_words[1] if len(street_words) > 1 else ""
                        if len(street_words) >= 3:
                            data[f"{prefix}_address_street_no"] = street_words[2]
                            data[f"{prefix}_address_street_name"] = " ".join(street_words[3:])
                    else:
                        # First word is likely street number
                        data[f"{prefix}_address_street_no"] = street_words[0]
                        data[f"{prefix}_address_street_name"] = " ".join(street_words[1:])
                
                # Suburb (usually second part)
                if len(address_parts) >= 2:
                    suburb_state_post = address_parts[1].strip()
                    suburb_words = suburb_state_post.split()
                    if len(suburb_words) >= 3:
                        data[f"{prefix}_address_suburb"] = " ".join(suburb_words[:-2])
                        data[f"{prefix}_address_state"] = suburb_words[-2]
                        data[f"{prefix}_address_postcode"] = suburb_words[-1]
        
        # Employment
        if borrower.job_title:
            data[f"{prefix}_occupation"] = borrower.job_title
        if borrower.employer_name:
            data[f"{prefix}_employer"] = borrower.employer_name
        if borrower.annual_income:
            data[f"{prefix}_annual_income"] = str(borrower.annual_income)
    
    # Get guarantors (treated as additional individuals)
    guarantors = application.guarantors.all()
    if guarantors.exists():
        # For now, map first guarantor to borrower2 if borrower2 slot is available
        if borrower_count < 2 and guarantors.first():
            guarantor = guarantors.first()
            prefix = "borrower2"
            
            if guarantor.title:
                data[f"{prefix}_title"] = guarantor.title.title()
            if guarantor.first_name:
                data[f"{prefix}_given_names"] = guarantor.first_name
            if guarantor.last_name:
                data[f"{prefix}_surname"] = guarantor.last_name
            
            # Date of birth
            if guarantor.date_of_birth:
                dob = guarantor.date_of_birth
                data[f"{prefix}_dob_day"] = str(dob.day)
                data[f"{prefix}_dob_month"] = str(dob.month)
                data[f"{prefix}_dob_year"] = str(dob.year)
            
            # Contact info
            if guarantor.home_phone:
                data[f"{prefix}_phone"] = guarantor.home_phone
            if guarantor.mobile:
                data[f"{prefix}_mobile"] = guarantor.mobile
            if guarantor.email:
                data[f"{prefix}_email"] = guarantor.email
            
            # Address
            if guarantor.address_unit:
                data[f"{prefix}_address_unit"] = guarantor.address_unit
            if guarantor.address_street_no:
                data[f"{prefix}_address_street_no"] = guarantor.address_street_no
            if guarantor.address_street_name:
                data[f"{prefix}_address_street_name"] = guarantor.address_street_name
            if guarantor.address_suburb:
                data[f"{prefix}_address_suburb"] = guarantor.address_suburb
            if guarantor.address_state:
                data[f"{prefix}_address_state"] = guarantor.address_state
            if guarantor.address_postcode:
                data[f"{prefix}_address_postcode"] = guarantor.address_postcode
            
            # Employment
            if guarantor.occupation:
                data[f"{prefix}_occupation"] = guarantor.occupation
            if guarantor.employer_name:
                data[f"{prefix}_employer"] = guarantor.employer_name
            if guarantor.annual_income:
                data[f"{prefix}_annual_income"] = str(guarantor.annual_income)
    
    # Get security properties
    security_properties = application.security_properties.all()
    for i, prop in enumerate(security_properties[:3]):  # Limit to 3 properties
        prop_num = i + 1
        prefix = f"security{prop_num}"
        
        # Address
        if prop.address_unit:
            data[f"{prefix}_unit"] = prop.address_unit
        if prop.address_street_no:
            data[f"{prefix}_street_no"] = prop.address_street_no
        if prop.address_street_name:
            data[f"{prefix}_street_name"] = prop.address_street_name
        if prop.address_suburb:
            data[f"{prefix}_suburb"] = prop.address_suburb
        if prop.address_state:
            data[f"{prefix}_state"] = prop.address_state
        if prop.address_postcode:
            data[f"{prefix}_postcode"] = prop.address_postcode
        
        # Mortgage details
        if prop.current_mortgagee:
            data[f"{prefix}_mortgagee1"] = prop.current_mortgagee
        if prop.first_mortgage:
            data[f"{prefix}_debt1"] = prop.first_mortgage
        if prop.second_mortgage:
            data[f"{prefix}_debt2"] = prop.second_mortgage
        
        # Valuation
        if prop.estimated_value:
            data[f"{prefix}_current_value"] = str(prop.estimated_value)
        if prop.purchase_price:
            data[f"{prefix}_purchase_price"] = str(prop.purchase_price)
        
        # Property details
        if prop.bedrooms:
            data[f"{prefix}_bedrooms"] = str(prop.bedrooms)
        if prop.bathrooms:
            data[f"{prefix}_bathrooms"] = str(prop.bathrooms)
        if prop.car_spaces:
            data[f"{prefix}_car_spaces"] = str(prop.car_spaces)
        if prop.building_size:
            data[f"{prefix}_building_size"] = str(prop.building_size)
        if prop.land_size:
            data[f"{prefix}_land_size"] = str(prop.land_size)
    
    # Get loan requirements
    loan_requirements = application.loan_requirements.all()
    for i, req in enumerate(loan_requirements[:6]):  # Limit to 6 requirements
        req_num = i + 1
        if req.description:
            data[f"loan_purpose{req_num}_desc"] = req.description
        if req.amount:
            data[f"loan_purpose{req_num}_amount"] = str(req.amount)
    
    # Calculate total loan purposes
    total_amount = sum(req.amount for req in loan_requirements if req.amount)
    if total_amount:
        data["loan_purposes_total"] = str(total_amount)
    
    return data


def extract_checkbox_data(application: Application) -> Dict[str, bool]:
    """
    Extract checkbox data from Application model and related models
    Based on corrected checkbox mappings
    """
    data = {}
    
    # Company trustee status
    company_borrowers = application.borrowers.filter(is_company=True)
    if company_borrowers.exists():
        company = company_borrowers.first()
        
        # Trustee checkboxes
        if company.is_trustee is not None:
            data["is_trustee_yes"] = company.is_trustee
            data["is_trustee_no"] = not company.is_trustee
        
        if company.is_smsf_trustee is not None:
            data["is_smsf_trustee_yes"] = company.is_smsf_trustee
            data["is_smsf_trustee_no"] = not company.is_smsf_trustee
        
        # Director roles (if available)
        directors = company.directors.all()
        if directors.exists():
            director1 = directors[0] if len(directors) >= 1 else None
            director2 = directors[1] if len(directors) >= 2 else None
            
            if director1 and director1.roles:
                roles = director1.roles.lower()
                data["director1_role_director"] = "director" in roles
                data["director1_role_secretary"] = "secretary" in roles
                data["director1_role_public_officer"] = "public officer" in roles or "public_officer" in roles
            
            if director2 and director2.roles:
                roles = director2.roles.lower()
                data["director2_role_director"] = "director" in roles
                data["director2_role_secretary"] = "secretary" in roles
                data["director2_role_public_officer"] = "public officer" in roles or "public_officer" in roles
    
    # Employment types for individual borrowers
    individual_borrowers = application.borrowers.filter(is_company=False)
    borrower_count = 0
    
    for borrower in individual_borrowers[:2]:
        borrower_count += 1
        prefix = f"borrower{borrower_count}"
        
        if borrower.employment_type:
            emp_type = borrower.employment_type.lower()
            data[f"{prefix}_fulltime"] = emp_type == "full_time"
            data[f"{prefix}_parttime"] = emp_type == "part_time"
            data[f"{prefix}_casual"] = emp_type == "casual"
            data[f"{prefix}_contract"] = emp_type == "contractor" or emp_type == "contract"
    
    # Employment type for guarantors (if mapped to borrower2)
    guarantors = application.guarantors.all()
    if guarantors.exists() and borrower_count < 2:
        guarantor = guarantors.first()
        if guarantor.employment_type:
            emp_type = guarantor.employment_type.lower()
            data["borrower2_fulltime"] = emp_type == "full_time"
            data["borrower2_parttime"] = emp_type == "part_time"
            data["borrower2_casual"] = emp_type == "casual"
            data["borrower2_contract"] = emp_type == "contract"
    
    # Solvency enquiries
    data["pending_litigation_yes"] = application.has_pending_litigation
    data["pending_litigation_no"] = not application.has_pending_litigation
    data["unsatisfied_judgements_yes"] = application.has_unsatisfied_judgements
    data["unsatisfied_judgements_no"] = not application.has_unsatisfied_judgements
    data["been_bankrupt_yes"] = application.has_been_bankrupt
    data["been_bankrupt_no"] = not application.has_been_bankrupt
    data["refused_credit_yes"] = application.has_been_refused_credit
    data["refused_credit_no"] = not application.has_been_refused_credit
    data["ato_debt_yes"] = application.has_outstanding_ato_debt
    data["ato_debt_no"] = not application.has_outstanding_ato_debt
    data["tax_returns_yes"] = application.has_outstanding_tax_returns
    data["tax_returns_no"] = not application.has_outstanding_tax_returns
    data["payment_arrangements_yes"] = application.has_payment_arrangements
    data["payment_arrangements_no"] = not application.has_payment_arrangements
    
    # Property types for security properties
    security_properties = application.security_properties.all()
    for i, prop in enumerate(security_properties[:3]):
        prop_num = i + 1
        prefix = f"security{prop_num}"
        
        if prop.property_type:
            prop_type = prop.property_type.lower()
            data[f"{prefix}_residential"] = prop_type == "residential"
            data[f"{prefix}_commercial"] = prop_type == "commercial"
            data[f"{prefix}_rural"] = prop_type == "rural"
            data[f"{prefix}_industrial"] = prop_type == "industrial"
            data[f"{prefix}_vacant_land"] = prop_type == "land"
            data[f"{prefix}_other"] = prop_type == "other"
        
        # Property features
        if hasattr(prop, 'is_single_story'):
            data[f"{prefix}_single_story"] = prop.is_single_story
            data[f"{prefix}_double_story"] = not prop.is_single_story
        
        if hasattr(prop, 'has_garage'):
            data[f"{prefix}_garage"] = prop.has_garage
        if hasattr(prop, 'has_carport'):
            data[f"{prefix}_carport"] = prop.has_carport
        if hasattr(prop, 'has_off_street_parking'):
            data[f"{prefix}_off_street"] = prop.has_off_street_parking
        
        # Occupancy
        if prop.occupancy:
            data[f"{prefix}_owner_occupied"] = prop.occupancy == "owner_occupied"
            data[f"{prefix}_investment"] = prop.occupancy == "investment"
        
        # Valuation type (default to current value)
        data[f"{prefix}_valuation_current"] = True
        data[f"{prefix}_valuation_purchase"] = False
    
    # Loan purpose
    if application.loan_purpose:
        purpose = application.loan_purpose.lower()
        data["loan_purpose_purchase"] = purpose == "purchase"
        data["loan_purpose_refinance"] = purpose == "refinance"
        data["loan_purpose_construction"] = purpose == "construction"
        data["loan_purpose_equity_venture"] = purpose == "equity_release"
        data["loan_purpose_cash_out"] = "cash" in purpose
        data["loan_purpose_payout_debt"] = "debt" in purpose
        data["loan_purpose_other"] = purpose == "other"
    
    # Exit strategy
    if application.exit_strategy:
        exit_strat = application.exit_strategy.lower()
        data["exit_strategy_sale"] = exit_strat == "sale"
        data["exit_strategy_refinance"] = exit_strat == "refinance"
        data["exit_strategy_cash_flow"] = exit_strat == "income"
        data["exit_strategy_other"] = exit_strat == "other"
    
    # Other submissions (default to No)
    data["other_submissions_yes"] = False
    data["other_submissions_no"] = True
    
    return data


def format_date(date_obj) -> Optional[str]:
    """Format date object to DD/MM/YYYY string"""
    if date_obj:
        return date_obj.strftime("%d/%m/%Y")
    return None 