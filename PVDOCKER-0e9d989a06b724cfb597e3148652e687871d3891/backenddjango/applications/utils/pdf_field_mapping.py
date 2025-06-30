"""
PDF Field Mapping Utility

This module contains functions to map application data from the cascade API response
to PDF field IDs for form filling.
"""

from typing import Dict, Any, List, Optional
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


def safe_get(data: dict, key: str, default: any = "") -> any:
    """
    Safely get a value from a dict, with optional default. Handles None, missing keys, and non-dict input.
    """
    if not isinstance(data, dict):
        return default
    if key in data and data[key] is not None:
        return data[key]
    return default


def format_currency(value: Any) -> str:
    """
    Format a value as currency string.
    
    Args:
        value: The value to format
    
    Returns:
        Formatted currency string or empty string if invalid
    """
    if value is None or value == "":
        return ""
    try:
        if isinstance(value, str):
            value = float(value)
        return f"{value:,.2f}"
    except (ValueError, TypeError):
        return ""


def format_date_parts(date_str: str) -> tuple:
    """
    Extract day, month, year from a date string.
    
    Args:
        date_str: Date string in YYYY-MM-DD format
    
    Returns:
        Tuple of (day, month, year) as strings
    """
    if not date_str:
        return ("", "", "")
    try:
        parts = date_str.split('-')
        if len(parts) >= 3:
            return (parts[2], parts[1], parts[0])  # day, month, year
        elif len(parts) >= 2:
            return ("", parts[1], parts[0])  # month, year
        elif len(parts) >= 1:
            return ("", "", parts[0])  # year only
    except:
        pass
    return ("", "", "")


def get_asset_by_type(assets: List[Dict], asset_type: str) -> Optional[Dict]:
    """
    Get the first asset of a specific type.
    
    Args:
        assets: List of asset dictionaries
        asset_type: The type of asset to find
    
    Returns:
        Asset dictionary or None if not found
    """
    for asset in assets:
        if asset.get('asset_type') == asset_type:
            return asset
    return None


def get_liability_by_type(liabilities: List[Dict], liability_type: str) -> Optional[Dict]:
    """
    Get the first liability of a specific type.
    
    Args:
        liabilities: List of liability dictionaries
        liability_type: The type of liability to find
    
    Returns:
        Liability dictionary or None if not found
    """
    for liability in liabilities:
        if liability.get('liability_type') == liability_type:
            return liability
    return None


def generate_pdf_field_mapping_from_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate PDF field mapping from cascade API response.
    
    This function maps the comprehensive application data returned by the
    cascade endpoint to PDF field IDs for form filling.
    
    Args:
        data: The cascade API response dictionary containing:
            - loan_amount, loan_term, interest_rate, etc. (at root level)
            - borrowers: List of individual borrowers
            - company_borrowers: List of company borrowers
            - guarantors: List of guarantors
            - security_properties: List of security properties
            - loan_requirements: List of loan requirements
    
    Returns:
        Dictionary mapping PDF field IDs to values
    """
    mapping = {}
    
    try:
        # Get main data sections - application fields are now at root level
        borrowers = data.get('borrowers', [])
        company_borrowers = data.get('company_borrowers', [])
        guarantors = data.get('guarantors', [])
        security_properties = data.get('security_properties', [])
        loan_requirements = data.get('loan_requirements', [])
        
        # Check if we have any data to process
        if not data and not borrowers and not company_borrowers and not guarantors and not security_properties:
            return {}
        
        # ============================================================================
        # SECTION 1: COMPANY BORROWER DETAILS
        # ============================================================================
        
        if company_borrowers:
            company = company_borrowers[0]  # First company borrower
            
            # Company basic details
            mapping['text1'] = safe_get(company, 'company_name')
            mapping['text2'] = safe_get(company, 'company_abn') or safe_get(company, 'company_acn')
            mapping['text3'] = safe_get(company, 'industry_type')
            mapping['text4'] = safe_get(company, 'contact_number')
            mapping['text5'] = format_currency(safe_get(company, 'annual_company_income'))
            
            # Trustee information
            mapping['checkbox20'] = "Yes" if safe_get(company, 'is_trustee', default=False) else ""
            mapping['checkbox21'] = "Yes" if not safe_get(company, 'is_trustee', default=False) else ""
            mapping['checkbox22'] = "Yes" if safe_get(company, 'is_smsf_trustee', default=False) else ""
            mapping['checkbox23'] = "Yes" if not safe_get(company, 'is_smsf_trustee', default=False) else ""
            mapping['text6'] = safe_get(company, 'trustee_name')
            
            # Director 1 Details
            directors = safe_get(company, 'directors', default=[])
            if directors:
                director1 = directors[0]
                mapping['text7'] = safe_get(director1, 'name', '')
                mapping['checkbox24'] = "Yes" if 'director' in safe_get(director1, 'roles', default='').lower() else ""
                mapping['checkbox25'] = "Yes" if 'secretary' in safe_get(director1, 'roles', default='').lower() else ""
                mapping['checkbox26'] = "Yes" if 'public_officer' in safe_get(director1, 'roles', default='').lower() else ""
                
                # Director ID (split into individual digits)
                director_id = safe_get(director1, 'director_id', default="")
                for i, digit in enumerate(director_id[:12]):
                    mapping[f'text{8 + i}'] = digit
                for i in range(len(director_id), 12):
                    mapping[f'text{8 + i}'] = ""
            
            # Director 2 Details
            if len(directors) > 1:
                director2 = directors[1]
                mapping['text30'] = safe_get(director2, 'name', '')
                mapping['checkbox27'] = "Yes" if 'director' in safe_get(director2, 'roles', default='').lower() else ""
                mapping['checkbox28'] = "Yes" if 'secretary' in safe_get(director2, 'roles', default='').lower() else ""
                mapping['checkbox29'] = "Yes" if 'public_officer' in safe_get(director2, 'roles', default='').lower() else ""
                
                # Director ID (split into individual digits)
                director_id = safe_get(director2, 'director_id', default="")
                for i, digit in enumerate(director_id[:12]):
                    mapping[f'text{31 + i}'] = digit
                for i in range(len(director_id), 12):
                    mapping[f'text{31 + i}'] = ""
            
            # Registered Business Address
            mapping['text43'] = safe_get(company, 'registered_address_unit')
            mapping['text44'] = safe_get(company, 'registered_address_street_no')
            mapping['text45'] = safe_get(company, 'registered_address_street_name')
            mapping['text46'] = safe_get(company, 'registered_address_suburb')
            mapping['text47'] = safe_get(company, 'registered_address_state')
            mapping['text48'] = safe_get(company, 'registered_address_postcode')
        
        # ============================================================================
        # SECTION 2: COMPANY ASSETS & LIABILITIES
        # ============================================================================
        
        if company_borrowers:
            company = company_borrowers[0]
            company_assets = safe_get(company, 'assets', default=[])
            company_liabilities = safe_get(company, 'liabilities', default=[])
            
            # Properties (up to 4)
            property_assets = [asset for asset in company_assets if asset.get('asset_type') == 'Property']
            for i, prop in enumerate(property_assets[:4]):
                base_idx = 49 + (i * 14)  # 49, 63, 77, 91
                mapping[f'text{base_idx}'] = safe_get(prop, 'address')
                mapping[f'text{base_idx + 1}'] = format_currency(safe_get(prop, 'value'))
                mapping[f'text{base_idx + 2}'] = format_currency(safe_get(prop, 'amount_owing'))
                mapping[f'checkbox{base_idx + 3}'] = safe_get(prop, 'to_be_refinanced', default=False)
            
            # Other Assets & Liabilities
            # Vehicles
            vehicle_asset = get_asset_by_type(company_assets, 'Vehicle')
            mapping['text65'] = format_currency(safe_get(vehicle_asset, 'value'))
            mapping['text66'] = format_currency(safe_get(vehicle_asset, 'amount_owing'))
            mapping['checkbox86'] = "Yes" if safe_get(vehicle_asset, 'to_be_refinanced', default=False) else ""
            
            # Savings
            savings_asset = get_asset_by_type(company_assets, 'Savings')
            mapping['text67'] = format_currency(safe_get(savings_asset, 'value'))
            mapping['text68'] = format_currency(safe_get(savings_asset, 'amount_owing'))
            mapping['checkbox87'] = "Yes" if safe_get(savings_asset, 'to_be_refinanced', default=False) else ""
            
            # Investment Shares
            shares_asset = get_asset_by_type(company_assets, 'Investment Shares')
            mapping['text69'] = format_currency(safe_get(shares_asset, 'value'))
            mapping['text70'] = format_currency(safe_get(shares_asset, 'amount_owing'))
            mapping['checkbox88'] = "Yes" if safe_get(shares_asset, 'to_be_refinanced', default=False) else ""
            
            # Credit Cards
            credit_card_liability = get_liability_by_type(company_liabilities, 'credit_card')
            mapping['text71'] = format_currency(safe_get(credit_card_liability, 'amount'))
            mapping['text72'] = format_currency(safe_get(credit_card_liability, 'amount'))
            mapping['checkbox89'] = "Yes" if safe_get(credit_card_liability, 'to_be_refinanced', default=False) else ""
            
            # Other Creditors
            other_creditor_liability = get_liability_by_type(company_liabilities, 'other_creditor')
            mapping['text73'] = format_currency(safe_get(other_creditor_liability, 'amount'))
            mapping['text74'] = format_currency(safe_get(other_creditor_liability, 'amount'))
            mapping['checkbox90'] = "Yes" if safe_get(other_creditor_liability, 'to_be_refinanced', default=False) else ""
            
            # Other
            other_asset = get_asset_by_type(company_assets, 'Other')
            mapping['text75'] = format_currency(safe_get(other_asset, 'value'))
            mapping['text76'] = format_currency(safe_get(other_asset, 'amount_owing'))
            mapping['checkbox91'] = "Yes" if safe_get(other_asset, 'to_be_refinanced', default=False) else ""
            
            # Totals
            total_assets = sum(float(asset.get('value', 0) or 0) for asset in company_assets)
            total_liabilities = sum(float(liability.get('amount', 0) or 0) for liability in company_liabilities)
            mapping['text77'] = format_currency(total_assets)
            mapping['text78'] = format_currency(total_liabilities)
        
        # ============================================================================
        # SECTION 3: GENERAL SOLVENCY ENQUIRIES
        # ============================================================================
        
        # Application fields are now at root level
        mapping['checkbox92'] = "Yes" if safe_get(data, 'has_pending_litigation', default=False) else ""
        mapping['checkbox93'] = "Yes" if not safe_get(data, 'has_pending_litigation', default=False) else ""
        mapping['checkbox94'] = "Yes" if safe_get(data, 'has_unsatisfied_judgements', default=False) else ""
        mapping['checkbox95'] = "Yes" if not safe_get(data, 'has_unsatisfied_judgements', default=False) else ""
        mapping['checkbox96'] = "Yes" if safe_get(data, 'has_been_bankrupt', default=False) else ""
        mapping['checkbox97'] = "Yes" if not safe_get(data, 'has_been_bankrupt', default=False) else ""
        mapping['checkbox98'] = "Yes" if safe_get(data, 'has_been_refused_credit', default=False) else ""
        mapping['checkbox99'] = "Yes" if not safe_get(data, 'has_been_refused_credit', default=False) else ""
        mapping['checkbox100'] = "Yes" if safe_get(data, 'has_outstanding_ato_debt', default=False) else ""
        mapping['checkbox101'] = "Yes" if not safe_get(data, 'has_outstanding_ato_debt', default=False) else ""
        mapping['checkbox102'] = "Yes" if safe_get(data, 'has_outstanding_tax_returns', default=False) else ""
        mapping['checkbox103'] = "Yes" if not safe_get(data, 'has_outstanding_tax_returns', default=False) else ""
        mapping['checkbox104'] = "Yes" if safe_get(data, 'has_payment_arrangements', default=False) else ""
        mapping['checkbox105'] = "Yes" if not safe_get(data, 'has_payment_arrangements', default=False) else ""
        
        # ============================================================================
        # SECTION 4: INDIVIDUAL DETAILS (Borrowers/Guarantors)
        # ============================================================================
        
        # Intelligent mapping for Section 4: Individual Details
        # Business Logic:
        # 1. If two individual borrowers exist → map both borrowers
        # 2. If one individual borrower + one guarantor exist → map borrower (1) + guarantor (2)
        # 3. If only two guarantors exist → map both guarantors
        # 4. If only one individual exists → map that individual to slot 1
        
        # Get individual borrowers (non-company borrowers)
        individual_borrowers = [b for b in borrowers if not safe_get(b, 'is_company', default=False)]
        individual_guarantors = [g for g in guarantors if safe_get(g, 'guarantor_type', default='') == 'individual']
        
        # Determine which individuals to map to the two slots
        individuals_to_map = []
        
        if len(individual_borrowers) >= 2:
            # Case 1: Two or more individual borrowers → map first two borrowers
            individuals_to_map = individual_borrowers[:2]
        elif len(individual_borrowers) == 1 and len(individual_guarantors) >= 1:
            # Case 2: One borrower + one or more guarantors → map borrower + first guarantor
            individuals_to_map = [individual_borrowers[0], individual_guarantors[0]]
        elif len(individual_guarantors) >= 2:
            # Case 3: Two or more guarantors → map first two guarantors
            individuals_to_map = individual_guarantors[:2]
        elif len(individual_borrowers) == 1:
            # Case 4: Only one individual borrower → map to slot 1
            individuals_to_map = [individual_borrowers[0]]
        elif len(individual_guarantors) == 1:
            # Case 5: Only one guarantor → map to slot 1
            individuals_to_map = [individual_guarantors[0]]
        
        # Map individuals to the two available slots
        logger.debug(f"=== INDIVIDUAL MAPPING DEBUG ===")
        logger.debug(f"Individual borrowers count: {len(individual_borrowers)}")
        logger.debug(f"Individual guarantors count: {len(individual_guarantors)}")
        logger.debug(f"Individuals to map: {len(individuals_to_map)}")
        for i, ind in enumerate(individuals_to_map):
            logger.debug(f"  Individual {i+1}: {ind.get('first_name', 'Unknown')} {ind.get('last_name', 'Unknown')} - Type: {'Borrower' if ind in individual_borrowers else 'Guarantor'} - Employment: {ind.get('employment_type', 'Unknown')}")
        
        for slot_idx, individual in enumerate(individuals_to_map[:2]):
            logger.debug(f"=== PROCESSING SLOT {slot_idx + 1} ===")
            logger.debug(f"Individual: {individual.get('first_name', 'Unknown')} {individual.get('last_name', 'Unknown')}")
            logger.debug(f"Employment type: {individual.get('employment_type', 'Unknown')}")
            if slot_idx == 0:
                # Individual 1 (fields 106-128)
                base_field = 106
                employment_checkbox_base = 124  # FIXED: Correct checkbox numbers for Borrower 1
                annual_income_field = 128
                logger.debug(f"Slot {slot_idx + 1} -> Individual 1 -> Checkboxes {employment_checkbox_base}-{employment_checkbox_base+3}")
            else:
                # Individual 2 (fields 129-151)
                base_field = 129
                employment_checkbox_base = 147
                annual_income_field = 151
                logger.debug(f"Slot {slot_idx + 1} -> Individual 2 -> Checkboxes {employment_checkbox_base}-{employment_checkbox_base+3}")
            
            # Personal Information
            mapping[f'text{base_field}'] = safe_get(individual, 'title')
            mapping[f'text{base_field + 1}'] = safe_get(individual, 'first_name')
            mapping[f'text{base_field + 2}'] = safe_get(individual, 'last_name')
            
            # Date of Birth
            dob = safe_get(individual, 'date_of_birth')
            day, month, year = format_date_parts(dob)
            mapping[f'text{base_field + 3}'] = day
            mapping[f'text{base_field + 4}'] = month
            mapping[f'text{base_field + 5}'] = year
            
            # Contact Information
            mapping[f'text{base_field + 6}'] = safe_get(individual, 'drivers_licence_no')
            mapping[f'text{base_field + 7}'] = safe_get(individual, 'home_phone')
            mapping[f'text{base_field + 8}'] = safe_get(individual, 'mobile')
            mapping[f'text{base_field + 9}'] = safe_get(individual, 'email')
            
            # Residential Address
            mapping[f'text{base_field + 10}'] = safe_get(individual, 'address_unit')
            mapping[f'text{base_field + 11}'] = safe_get(individual, 'address_street_no')
            mapping[f'text{base_field + 12}'] = safe_get(individual, 'address_street_name')
            mapping[f'text{base_field + 13}'] = safe_get(individual, 'address_suburb')
            mapping[f'text{base_field + 14}'] = safe_get(individual, 'address_state')
            mapping[f'text{base_field + 15}'] = safe_get(individual, 'address_postcode')
            
            # Employment Information
            mapping[f'text{base_field + 16}'] = safe_get(individual, 'occupation')
            mapping[f'text{base_field + 17}'] = safe_get(individual, 'employer_name')
            
            # Employment Type Checkboxes
            employment_type = safe_get(individual, 'employment_type', default='')
            logger.debug(f"Individual {slot_idx + 1} employment_type: '{employment_type}'")
            
            # Map employment type to checkboxes - handle both 'contract' and 'contractor'
            is_full_time = employment_type == 'full_time'
            is_part_time = employment_type == 'part_time'
            is_casual = employment_type == 'casual'
            is_contract = employment_type in ['contract', 'contractor']
            
            # Convert boolean to "Yes" for PDF checkbox compatibility
            mapping[f'checkbox{employment_checkbox_base}'] = "Yes" if is_full_time else ""
            mapping[f'checkbox{employment_checkbox_base + 1}'] = "Yes" if is_part_time else ""
            mapping[f'checkbox{employment_checkbox_base + 2}'] = "Yes" if is_casual else ""
            mapping[f'checkbox{employment_checkbox_base + 3}'] = "Yes" if is_contract else ""
            
            logger.debug(f"Individual {slot_idx + 1} employment checkboxes: full_time={is_full_time}, part_time={is_part_time}, casual={is_casual}, contract={is_contract}")
            logger.debug(f"Individual {slot_idx + 1} checkbox fields: checkbox{employment_checkbox_base}={mapping[f'checkbox{employment_checkbox_base}']}, checkbox{employment_checkbox_base + 1}={mapping[f'checkbox{employment_checkbox_base + 1}']}, checkbox{employment_checkbox_base + 2}={mapping[f'checkbox{employment_checkbox_base + 2}']}, checkbox{employment_checkbox_base + 3}={mapping[f'checkbox{employment_checkbox_base + 3}']}")
            logger.debug(f"=== FINAL CHECKBOX VALUES FOR SLOT {slot_idx + 1} ===")
            logger.debug(f"checkbox{employment_checkbox_base} (Full Time): {mapping[f'checkbox{employment_checkbox_base}']}")
            logger.debug(f"checkbox{employment_checkbox_base + 1} (Part Time): {mapping[f'checkbox{employment_checkbox_base + 1}']}")
            logger.debug(f"checkbox{employment_checkbox_base + 2} (Casual): {mapping[f'checkbox{employment_checkbox_base + 2}']}")
            logger.debug(f"checkbox{employment_checkbox_base + 3} (Contract): {mapping[f'checkbox{employment_checkbox_base + 3}']}")
            logger.debug(f"=== END SLOT {slot_idx + 1} ===")
            
            # Make sure text120 is mapped for the first individual (occupation field)
            if slot_idx == 0:
                mapping['text120'] = safe_get(individual, 'occupation', '')
            
            # Annual Income
            mapping[f'text{annual_income_field}'] = format_currency(safe_get(individual, 'annual_income'))
        
        # ============================================================================
        # EXPLICIT FIRST INDIVIDUAL EMPLOYMENT CHECKBOX MAPPING (124-127)
        # ============================================================================
        
        # Ensure first individual employment checkboxes are always mapped correctly
        if individuals_to_map:
            first_individual = individuals_to_map[0]
            employment_type = safe_get(first_individual, 'employment_type', default='')
            logger.debug(f"=== EXPLICIT FIRST INDIVIDUAL EMPLOYMENT MAPPING ===")
            logger.debug(f"First individual: {first_individual.get('first_name', 'Unknown')} {first_individual.get('last_name', 'Unknown')}")
            logger.debug(f"Employment type: '{employment_type}'")
            
            # Map employment type to checkboxes - handle both 'contract' and 'contractor'
            is_full_time = employment_type == 'full_time'
            is_part_time = employment_type == 'part_time'
            is_casual = employment_type == 'casual'
            is_contract = employment_type in ['contract', 'contractor']
            
            # Based on PDF inspection, the actual employment checkboxes for first individual are:
            # These are the checkboxes at coordinates [27.8182, 410.829], [90.9818, 410.829], etc.
            # They have Parent objects with IDs 838, 835, 836, 837
            
            # Explicit mapping for first individual employment checkboxes
            # Try multiple formats to ensure compatibility with the PDF form
            
            # Format 1: checkbox124 (our standard format) - use "Yes" for PDF compatibility
            mapping['checkbox124'] = "Yes" if is_full_time else ""
            mapping['checkbox125'] = "Yes" if is_part_time else ""
            mapping['checkbox126'] = "Yes" if is_casual else ""
            mapping['checkbox127'] = "Yes" if is_contract else ""
            
            # Format 2: Check Box124 (PDF's format) - use "Yes" for PDF compatibility
            mapping['Check Box124'] = "Yes" if is_full_time else ""
            mapping['Check Box125'] = "Yes" if is_part_time else ""
            mapping['Check Box126'] = "Yes" if is_casual else ""
            mapping['Check Box127'] = "Yes" if is_contract else ""
            
            # Format 3: Try mapping to the actual checkbox IDs from the PDF inspection
            # These are the parent IDs of the checkboxes we found in the PDF
            mapping['parent838'] = "Yes" if is_full_time else ""
            mapping['parent835'] = "Yes" if is_part_time else ""
            mapping['parent836'] = "Yes" if is_casual else ""
            mapping['parent837'] = "Yes" if is_contract else ""
            
            # Make sure text120 is explicitly mapped (occupation field)
            mapping['text120'] = safe_get(first_individual, 'occupation', '')
            
            logger.debug(f"Explicit checkbox mapping:")
            logger.debug(f"  checkbox124 (Full Time): {mapping['checkbox124']}")
            logger.debug(f"  checkbox125 (Part Time): {mapping['checkbox125']}")
            logger.debug(f"  checkbox126 (Casual/Temp): {mapping['checkbox126']}")
            logger.debug(f"  checkbox127 (Contract): {mapping['checkbox127']}")
            logger.debug(f"  text120 (Occupation): {mapping['text120']}")
            logger.debug(f"=== END EXPLICIT FIRST INDIVIDUAL MAPPING ===")
        
        # ============================================================================
        # SECTION 5: GUARANTOR ASSETS & LIABILITIES
        # ============================================================================
        
        # FIXED: Combine assets and liabilities from ALL individuals (borrowers + guarantors)
        all_individual_assets = []
        all_individual_liabilities = []
        
        # Add assets and liabilities from individual borrowers
        for borrower in borrowers:
            all_individual_assets.extend(safe_get(borrower, 'assets', default=[]))
            all_individual_liabilities.extend(safe_get(borrower, 'liabilities', default=[]))
        
        # Add assets and liabilities from guarantors
        for guarantor in guarantors:
            all_individual_assets.extend(safe_get(guarantor, 'assets', default=[]))
            all_individual_liabilities.extend(safe_get(guarantor, 'liabilities', default=[]))
        
        # Property Assets (up to 4)
        property_assets = [asset for asset in all_individual_assets if asset.get('asset_type') == 'Property']
        property_field_map = [
            (152, 155, 156),  # Property 1: text152, text153, text154, checkbox155, checkbox156
            (157, 180, 181),  # Property 2: text157, text158, text159, checkbox180, checkbox181
            (160, 182, 183),  # Property 3: text160, text161, text162, checkbox182, checkbox183
            (163, 184, 185),  # Property 4: text163, text164, text165, checkbox184, checkbox185
        ]
        for i, prop in enumerate(property_assets[:4]):
            addr_idx, bg1_idx, bg2_idx = property_field_map[i]
            mapping[f'text{addr_idx}'] = safe_get(prop, 'address')
            mapping[f'text{addr_idx+1}'] = format_currency(safe_get(prop, 'value'))
            mapping[f'text{addr_idx+2}'] = format_currency(safe_get(prop, 'amount_owing'))
            bg_type = safe_get(prop, 'bg_type', 'BG1')
            mapping[f'checkbox{bg1_idx}'] = bg_type == 'BG1'
            mapping[f'checkbox{bg2_idx}'] = bg_type == 'BG2'
        
        # Other Asset & Liability Types
        # Vehicles
        vehicle_asset = get_asset_by_type(all_individual_assets, 'Vehicle')
        mapping['text166'] = format_currency(safe_get(vehicle_asset, 'value'))
        mapping['text167'] = format_currency(safe_get(vehicle_asset, 'amount_owing'))
        bg_type = safe_get(vehicle_asset, 'bg_type', 'BG1')
        mapping['checkbox186'] = "Yes" if bg_type == 'BG1' else ""
        mapping['checkbox187'] = "Yes" if bg_type == 'BG2' else ""
        
        # Savings
        savings_asset = get_asset_by_type(all_individual_assets, 'Savings')
        mapping['text168'] = format_currency(safe_get(savings_asset, 'value'))
        mapping['text169'] = format_currency(safe_get(savings_asset, 'amount_owing'))
        bg_type = safe_get(savings_asset, 'bg_type', 'BG1')
        mapping['checkbox188'] = "Yes" if bg_type == 'BG1' else ""
        mapping['checkbox189'] = "Yes" if bg_type == 'BG2' else ""
        
        # Investment Shares
        shares_asset = get_asset_by_type(all_individual_assets, 'Investment Shares')
        mapping['text170'] = format_currency(safe_get(shares_asset, 'value'))
        mapping['text171'] = format_currency(safe_get(shares_asset, 'amount_owing'))
        bg_type = safe_get(shares_asset, 'bg_type', 'BG1')
        mapping['checkbox190'] = "Yes" if bg_type == 'BG1' else ""
        mapping['checkbox191'] = "Yes" if bg_type == 'BG2' else ""
        
        # Credit Cards
        credit_card_liability = get_liability_by_type(all_individual_liabilities, 'credit_card')
        mapping['text172'] = format_currency(safe_get(credit_card_liability, 'amount'))
        mapping['text173'] = format_currency(safe_get(credit_card_liability, 'amount'))
        bg_type = safe_get(credit_card_liability, 'bg_type', 'bg1')
        mapping['checkbox192'] = "Yes" if bg_type == 'bg1' else ""
        mapping['checkbox193'] = "Yes" if bg_type == 'bg2' else ""
        
        # Other Creditors
        other_creditor_liability = get_liability_by_type(all_individual_liabilities, 'other_creditor')
        mapping['text174'] = format_currency(safe_get(other_creditor_liability, 'amount'))
        mapping['text175'] = format_currency(safe_get(other_creditor_liability, 'amount'))
        bg_type = safe_get(other_creditor_liability, 'bg_type', 'bg1')
        mapping['checkbox194'] = "Yes" if bg_type == 'bg1' else ""
        mapping['checkbox195'] = "Yes" if bg_type == 'bg2' else ""
        
        # Other
        other_asset = get_asset_by_type(all_individual_assets, 'Other')
        mapping['text176'] = format_currency(safe_get(other_asset, 'value'))
        mapping['text177'] = format_currency(safe_get(other_asset, 'amount_owing'))
        bg_type = safe_get(other_asset, 'bg_type', 'BG1')
        mapping['checkbox196'] = "Yes" if bg_type == 'BG1' else ""
        mapping['checkbox197'] = "Yes" if bg_type == 'BG2' else ""
        
        # Totals
        total_individual_assets = sum(float(asset.get('value', 0) or 0) for asset in all_individual_assets)
        total_individual_liabilities = sum(float(liability.get('amount', 0) or 0) for liability in all_individual_liabilities)
        mapping['text178'] = format_currency(total_individual_assets)
        mapping['text179'] = format_currency(total_individual_liabilities)
        
        # ============================================================================
        # SECTION 6: PROPOSED SECURITY DETAILS (up to 3 properties)
        # ============================================================================
        
        for i, prop in enumerate(security_properties[:3]):
            base_idx = 198 + (i * 33)  # 198, 231, 264
            
            # Address
            mapping[f'text{base_idx}'] = safe_get(prop, 'address_unit')
            mapping[f'text{base_idx + 1}'] = safe_get(prop, 'address_street_no')
            mapping[f'text{base_idx + 2}'] = safe_get(prop, 'address_street_name')
            mapping[f'text{base_idx + 3}'] = safe_get(prop, 'address_suburb')
            mapping[f'text{base_idx + 4}'] = safe_get(prop, 'address_state')
            mapping[f'text{base_idx + 5}'] = safe_get(prop, 'address_postcode')
            
            # Current Mortgagee
            mapping[f'text{base_idx + 6}'] = format_currency(safe_get(prop, 'first_mortgage'))
            mapping[f'text{base_idx + 7}'] = format_currency(safe_get(prop, 'second_mortgage'))
            
            # Current Debt Position
            mapping[f'text{base_idx + 8}'] = format_currency(safe_get(prop, 'first_mortgage_debt'))
            mapping[f'text{base_idx + 9}'] = format_currency(safe_get(prop, 'second_mortgage_debt'))
            
            # Valuation
            mapping[f'checkbox{base_idx + 10}'] = "Yes"  # Est. Current Value tick
            mapping[f'text{base_idx + 12}'] = format_currency(safe_get(prop, 'estimated_value'))
            mapping[f'checkbox{base_idx + 11}'] = "Yes"  # Purchase Price tick
            mapping[f'text{base_idx + 13}'] = format_currency(safe_get(prop, 'purchase_price'))
            
            # Property Type
            prop_type = safe_get(prop, 'property_type', default='')
            mapping[f'checkbox{base_idx + 14}'] = "Yes" if prop_type == 'residential' else ""
            mapping[f'checkbox{base_idx + 15}'] = "Yes" if prop_type == 'commercial' else ""
            mapping[f'checkbox{base_idx + 16}'] = "Yes" if prop_type == 'rural' else ""
            mapping[f'checkbox{base_idx + 17}'] = "Yes" if prop_type == 'industrial' else ""
            mapping[f'checkbox{base_idx + 18}'] = "Yes" if prop_type == 'land' else ""
            mapping[f'checkbox{base_idx + 19}'] = "Yes" if prop_type == 'other' else ""
            mapping[f'text{base_idx + 20}'] = safe_get(prop, 'description_if_applicable') if prop_type == 'other' else ""
            
            # Description
            mapping[f'text{base_idx + 21}'] = str(safe_get(prop, 'bedrooms', default=""))
            mapping[f'text{base_idx + 22}'] = str(safe_get(prop, 'bathrooms', default=""))
            mapping[f'text{base_idx + 23}'] = str(safe_get(prop, 'car_spaces', default=""))
            mapping[f'text{base_idx + 24}'] = format_currency(safe_get(prop, 'building_size'))
            mapping[f'text{base_idx + 25}'] = format_currency(safe_get(prop, 'land_size'))
            
            # Property Features
            mapping[f'checkbox{base_idx + 26}'] = "Yes" if safe_get(prop, 'is_single_story', default=False) else ""
            mapping[f'checkbox{base_idx + 27}'] = "Yes" if not safe_get(prop, 'is_single_story', default=False) else ""  # Double story
            mapping[f'checkbox{base_idx + 28}'] = "Yes" if safe_get(prop, 'has_garage', default=False) else ""
            mapping[f'checkbox{base_idx + 29}'] = "Yes" if safe_get(prop, 'has_carport', default=False) else ""
            mapping[f'checkbox{base_idx + 30}'] = "Yes" if safe_get(prop, 'has_off_street_parking', default=False) else ""
            
            # Owner Type
            occupancy = safe_get(prop, 'occupancy', default='')
            mapping[f'checkbox{base_idx + 31}'] = "Yes" if occupancy == 'owner_occupied' else ""
            mapping[f'checkbox{base_idx + 32}'] = "Yes" if occupancy == 'investment' else ""
        
        # ============================================================================
        # SECTION 7: LOAN DETAILS & PURPOSE
        # ============================================================================
        
        # Application fields are now at root level
        mapping['text297'] = format_currency(safe_get(data, 'loan_amount'))
        mapping['text298'] = str(safe_get(data, 'loan_term', default=""))
        
        # Proposed Settlement Date
        settlement_date = safe_get(data, 'estimated_settlement_date')
        day, month, year = format_date_parts(settlement_date)
        mapping['text299'] = day
        mapping['text300'] = month
        mapping['text301'] = year
        
        mapping['text302'] = str(safe_get(data, 'interest_rate', default=""))
        
        # Loan Purpose
        loan_purpose = safe_get(data, 'loan_purpose', default='')
        mapping['checkbox303'] = "Yes" if loan_purpose == 'purchase' else ""
        mapping['checkbox304'] = "Yes" if loan_purpose == 'seed_capital' else ""
        mapping['checkbox305'] = "Yes" if loan_purpose == 'settlement_shortfall' else ""
        mapping['checkbox306'] = "Yes" if loan_purpose == 'equity_venture' else ""
        mapping['checkbox307'] = "Yes" if loan_purpose == 'cash_out' else ""
        mapping['checkbox308'] = "Yes" if loan_purpose == 'refinance' else ""
        mapping['checkbox309'] = "Yes" if loan_purpose == 'construction' else ""
        mapping['checkbox310'] = "Yes" if loan_purpose == 'payout_existing_debt' else ""
        mapping['checkbox311'] = "Yes" if loan_purpose == 'other' else ""
        
        mapping['text312'] = safe_get(data, 'additional_comments')
        
        # Disclosure of Other Submissions
        mapping['checkbox313'] = "Yes" if safe_get(data, 'has_other_credit_providers', default=False) else ""
        mapping['checkbox314'] = "Yes" if not safe_get(data, 'has_other_credit_providers', default=False) else ""
        mapping['text315'] = safe_get(data, 'other_credit_providers_details')
        
        # ============================================================================
        # SECTION 8: LOAN REQUIREMENTS
        # ============================================================================
        
        for i, req in enumerate(loan_requirements[:6]):
            mapping[f'text{316 + (i * 2)}'] = safe_get(req, 'description')
            mapping[f'text{317 + (i * 2)}'] = format_currency(safe_get(req, 'amount'))
        
        # Total Amount
        total_requirements = sum(float(req.get('amount', 0) or 0) for req in loan_requirements)
        mapping['text328'] = format_currency(total_requirements)
        
        # ============================================================================
        # SECTION 9: PROPOSED EXIT STRATEGY
        # ============================================================================
        
        exit_strategy = safe_get(data, 'exit_strategy', default='')
        mapping['checkbox329'] = "Yes" if exit_strategy == 'refinance' else ""
        mapping['checkbox330'] = "Yes" if exit_strategy == 'sale_of_security' else ""
        mapping['checkbox331'] = "Yes" if exit_strategy == 'cash_flow' else ""
        mapping['checkbox332'] = "Yes" if exit_strategy == 'other' else ""
        
        mapping['text333'] = safe_get(data, 'exit_strategy_details')
        
    except Exception as e:
        logger.error(f"Error generating PDF field mapping: {str(e)}")
        # Return empty mapping on error
        return {}
    
    # ============================================================================
    # VALIDATION AND DEBUGGING
    # ============================================================================
    
    # Validate critical fields are present
    critical_fields = [
        'text120',  # First individual occupation
        'checkbox124', 'checkbox125', 'checkbox126', 'checkbox127'  # First individual employment type
    ]
    
    for field in critical_fields:
        if field not in mapping:
            logger.warning(f"Critical field {field} is missing from mapping")
        else:
            logger.debug(f"Critical field {field} = {mapping[field]}")
    
    # Add coordinates for employment checkboxes to help with direct coordinate matching
    mapping['employment_checkboxes'] = [
        {
            'rect': ['27.8182', '410.829', '41.5636', '423.011'],
            'type': 'full_time',
            'field_id': 'checkbox124',
            'value': mapping.get('checkbox124', False)
        },
        {
            'rect': ['90.9818', '410.829', '104.727', '423.011'],
            'type': 'part_time',
            'field_id': 'checkbox125',
            'value': mapping.get('checkbox125', False)
        },
        {
            'rect': ['155.109', '410.175', '168.854', '422.357'],
            'type': 'casual',
            'field_id': 'checkbox126',
            'value': mapping.get('checkbox126', False)
        },
        {
            'rect': ['233.309', '409.52', '247.054', '421.702'],
            'type': 'contract',
            'field_id': 'checkbox127',
            'value': mapping.get('checkbox127', False)
        }
    ]
    
    logger.debug(f"PDF field mapping output: {mapping}")
    return mapping 