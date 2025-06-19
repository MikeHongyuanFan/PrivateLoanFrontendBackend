"""
PDF Form Field Mappings and Constants

This module contains all the static field mappings and constants used for
PDF form filling. Separating these constants makes the main PDF filler
logic cleaner and the mappings easier to maintain.

Field mappings are based on manual PDF examination and user analysis.
"""

from typing import Dict


# TEXT FIELD MAPPINGS - Based on actual PDF field names and meanings
FIELD_MAP: Dict[str, str] = {
    # SECTION 1: COMPANY BORROWER DETAILS
    "company_name": "Text1",                       # Company Name
    "company_abn_acn": "Text2",                    # ABN/ACN
    "company_industry_type": "Text3",              # Industry Type
    "company_contact_number": "Text4",             # Contact Number
    "annual_company_income": "Text5",              # Annual Company Income ($)
    "trustee_name": "Text6",                       # Trustee Name (if applicable)
    
    # Director 1 Details
    "director1_name": "Text7",                     # Director 1 → Full Name
    "director1_id_1": "Text8",                     # Director 1 → Director ID (digit 1)
    "director1_id_2": "Text9",                     # Director 1 → Director ID (digit 2)
    "director1_id_3": "Text10",                    # Director 1 → Director ID (digit 3)
    "director1_id_4": "Text11",                    # Director 1 → Director ID (digit 4)
    "director1_id_5": "Text12",                    # Director 1 → Director ID (digit 5)
    "director1_id_6": "Text13",                    # Director 1 → Director ID (digit 6)
    "director1_id_7": "Text14",                    # Director 1 → Director ID (digit 7)
    "director1_id_8": "Text15",                    # Director 1 → Director ID (digit 8)
    "director1_id_9": "Text16",                    # Director 1 → Director ID (digit 9)
    "director1_id_10": "Text17",                   # Director 1 → Director ID (digit 10)
    "director1_id_11": "Text18",                   # Director 1 → Director ID (digit 11)
    "director1_id_12": "Text19",                   # Director 1 → Director ID (digit 12)
    
    # Director 2 Details
    "director2_name": "Text30",                    # Director 2 → Full Name
    "director2_id_1": "Text31",                    # Director 2 → Director ID (digit 1)
    "director2_id_2": "Text32",                    # Director 2 → Director ID (digit 2)
    "director2_id_3": "Text33",                    # Director 2 → Director ID (digit 3)
    "director2_id_4": "Text34",                    # Director 2 → Director ID (digit 4)
    "director2_id_5": "Text35",                    # Director 2 → Director ID (digit 5)
    "director2_id_6": "Text36",                    # Director 2 → Director ID (digit 6)
    "director2_id_7": "Text37",                    # Director 2 → Director ID (digit 7)
    "director2_id_8": "Text38",                    # Director 2 → Director ID (digit 8)
    "director2_id_9": "Text39",                    # Director 2 → Director ID (digit 9)
    "director2_id_10": "Text40",                   # Director 2 → Director ID (digit 10)
    "director2_id_11": "Text41",                   # Director 2 → Director ID (digit 11)
    "director2_id_12": "Text42",                   # Director 2 → Director ID (digit 12)
    
    # Registered Business Address
    "company_address_unit": "Text43",              # Unit No.
    "company_address_street_no": "Text44",         # Street No.
    "company_address_street_name": "Text45",       # Street Name
    "company_address_suburb": "Text46",            # Suburb
    "company_address_state": "Text47",             # State
    "company_address_postcode": "Text48",          # Postcode
    
    # SECTION 2: COMPANY ASSETS & LIABILITIES
    # Properties (up to 4)
    "company_property1_address": "Text49",         # Property 1 → Address
    "company_property1_value": "Text50",           # Property 1 → Value ($)
    "company_property1_owing": "Text51",           # Property 1 → Amount Owing ($)
    "company_property2_address": "Text53",         # Property 2 → Address
    "company_property2_value": "Text54",           # Property 2 → Value ($)
    "company_property2_owing": "Text55",           # Property 2 → Amount Owing ($)
    "company_property3_address": "Text59",         # Property 3 → Address
    "company_property3_value": "Text60",           # Property 3 → Value ($)
    "company_property3_owing": "Text61",           # Property 3 → Amount Owing ($)
    "company_property4_address": "Text62",         # Property 4 → Address
    "company_property4_value": "Text63",           # Property 4 → Value ($)
    "company_property4_owing": "Text64",           # Property 4 → Amount Owing ($)
    
    # Other Assets & Liabilities
    "company_vehicles_value": "Text65",            # Vehicle(s) → Value ($)
    "company_vehicles_owing": "Text66",            # Vehicle(s) → Amount Owing ($)
    "company_savings_value": "Text67",             # Savings → Value ($)
    "company_savings_owing": "Text68",             # Savings → Amount Owing ($)
    "company_shares_value": "Text69",              # Investment Shares → Value ($)
    "company_shares_owing": "Text70",              # Investment Shares → Amount Owing ($)
    "company_creditcard_value": "Text71",          # Credit Card(s) → Value ($)
    "company_creditcard_owing": "Text72",          # Credit Card(s) → Amount Owing ($)
    "company_othercreditor_value": "Text73",       # Other Creditor(s) → Value ($)
    "company_othercreditor_owing": "Text74",       # Other Creditor(s) → Amount Owing ($)
    "company_other_value": "Text75",               # Other → Value ($)
    "company_other_owing": "Text76",               # Other → Amount Owing ($)
    
    # Company Asset Totals
    "company_total_assets": "Text77",              # Total Value of Assets ($)
    "company_total_owing": "Text78",               # Total Amount Owing ($)
    
    # SECTION 4: INDIVIDUAL DETAILS (Borrower/Guarantor 1)
    "borrower1_title": "Text106",                  # Title
    "borrower1_given_names": "Text107",            # Given Names
    "borrower1_surname": "Text108",                # Surname
    "borrower1_dob_day": "Text109",                # Date of Birth → Day
    "borrower1_dob_month": "Text110",              # Date of Birth → Month
    "borrower1_dob_year": "Text111",               # Date of Birth → Year
    "borrower1_licence": "Text112",                # Driver's Licence Number
    "borrower1_phone": "Text113",                  # Phone Number – Home
    "borrower1_mobile": "Text114",                 # Mobile Number
    "borrower1_email": "Text115",                  # Email Address
    "borrower1_address_unit": "Text116",           # Residential Address → Unit No.
    "borrower1_address_street_no": "Text117",      # Residential Address → Street No.
    "borrower1_address_street_name": "Text118",    # Residential Address → Street Name
    "borrower1_address_suburb": "Text119",         # Residential Address → Suburb
    "borrower1_address_state": "Text120",          # Residential Address → State
    "borrower1_address_postcode": "Text121",       # Residential Address → Postcode
    "borrower1_occupation": "Text122",             # Employment → Occupation
    "borrower1_employer": "Text123",               # Employer Name / Trading Name
    "borrower1_annual_income": "Text128",          # Annual Income (before tax)
    
    # SECTION 4: INDIVIDUAL DETAILS (Borrower/Guarantor 2)
    "borrower2_title": "Text129",                  # Title
    "borrower2_given_names": "Text130",            # Given Names
    "borrower2_surname": "Text131",                # Surname
    "borrower2_dob_day": "Text132",                # Date of Birth → Day
    "borrower2_dob_month": "Text133",              # Date of Birth → Month
    "borrower2_dob_year": "Text134",               # Date of Birth → Year
    "borrower2_licence": "Text135",                # Driver's Licence Number
    "borrower2_phone": "Text136",                  # Phone Number – Home
    "borrower2_mobile": "Text137",                 # Mobile Number
    "borrower2_email": "Text138",                  # Email Address
    "borrower2_address_unit": "Text139",           # Residential Address → Unit No.
    "borrower2_address_street_no": "Text140",      # Residential Address → Street No.
    "borrower2_address_street_name": "Text141",    # Residential Address → Street Name
    "borrower2_address_suburb": "Text142",         # Residential Address → Suburb
    "borrower2_address_state": "Text143",          # Residential Address → State
    "borrower2_address_postcode": "Text144",       # Residential Address → Postcode
    "borrower2_occupation": "Text145",             # Employment → Occupation
    "borrower2_employer": "Text146",               # Employer Name / Trading Name
    "borrower2_annual_income": "Text151",          # Annual Income (before tax)
    
    # SECTION 5: GUARANTOR ASSETS & LIABILITIES
    # Property Assets
    "guarantor_property1_address": "Text152",      # Property 1 → Address
    "guarantor_property1_value": "Text153",        # Property 1 → Value ($)
    "guarantor_property1_owing": "Text154",        # Property 1 → Amount Owing ($)
    "guarantor_property2_address": "Text157",      # Property 2 → Address
    "guarantor_property2_value": "Text158",        # Property 2 → Value ($)
    "guarantor_property2_owing": "Text159",        # Property 2 → Amount Owing ($)
    "guarantor_property3_address": "Text160",      # Property 3 → Address
    "guarantor_property3_value": "Text161",        # Property 3 → Value ($)
    "guarantor_property3_owing": "Text162",        # Property 3 → Amount Owing ($)
    "guarantor_property4_address": "Text163",      # Property 4 → Address
    "guarantor_property4_value": "Text164",        # Property 4 → Value ($)
    "guarantor_property4_owing": "Text165",        # Property 4 → Amount Owing ($)
    
    # Other Guarantor Assets & Liabilities
    "guarantor_vehicles_value": "Text166",         # Vehicle(s) → Value ($)
    "guarantor_vehicles_owing": "Text167",         # Vehicle(s) → Amount Owing ($)
    "guarantor_savings_value": "Text168",          # Savings → Value ($)
    "guarantor_savings_owing": "Text169",          # Savings → Amount Owing ($)
    "guarantor_shares_value": "Text170",           # Investment Shares → Value ($)
    "guarantor_shares_owing": "Text171",           # Investment Shares → Amount Owing ($)
    "guarantor_creditcard_value": "Text172",       # Credit Card(s) → Value ($)
    "guarantor_creditcard_owing": "Text173",       # Credit Card(s) → Amount Owing ($)
    "guarantor_othercreditor_value": "Text174",    # Other Creditor(s) → Value ($)
    "guarantor_othercreditor_owing": "Text175",    # Other Creditor(s) → Amount Owing ($)
    "guarantor_other_value": "Text176",            # Other → Value ($)
    "guarantor_other_owing": "Text177",            # Other → Amount Owing ($)
    
    # Guarantor Asset Totals
    "guarantor_total_assets": "Text178",           # Total Value of All Assets ($)
    "guarantor_total_owing": "Text179",            # Total Amount Owing on All Assets ($)
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 1
    "security1_unit": "Text198",                   # Unit No.
    "security1_street_no": "Text199",              # Street No.
    "security1_street_name": "Text200",            # Street Name
    "security1_suburb": "Text201",                 # Suburb
    "security1_state": "Text202",                  # State
    "security1_postcode": "Text203",               # Postcode
    "security1_mortgagee1": "Text204",             # Current Mortgagee Name – 1st Mortgage
    "security1_mortgagee2": "Text205",             # Current Mortgagee Name – 2nd Mortgage
    "security1_debt1": "Text206",                  # Current Debt Position – 1st Mortgage Amount
    "security1_debt2": "Text207",                  # Current Debt Position – 2nd Mortgage Amount
    "security1_current_value": "Text210",          # Est. Current Value – Value ($)
    "security1_purchase_price": "Text211",         # Purchase Price – Value ($)
    "security1_type_other": "Text218",             # If Other, specify
    "security1_bedrooms": "Text219",               # No. of Bedrooms
    "security1_bathrooms": "Text220",              # No. of Bathrooms
    "security1_car_spaces": "Text221",             # No. of Car Spaces
    "security1_building_size": "Text222",          # Building Size (sqm)
    "security1_land_size": "Text223",              # Land Size (sqm)
    
    # SECTION 6: PROPOSED SECURITY DETAILS - PROPERTY 2
    "security2_unit": "Text231",                   # Unit No.
    "security2_street_no": "Text232",              # Street No.
    "security2_street_name": "Text233",            # Street Name
    "security2_suburb": "Text234",                 # Suburb
    "security2_state": "Text235",                  # State
    "security2_postcode": "Text236",               # Postcode
    "security2_mortgagee1": "Text237",             # 1st Mortgage – Lender Name
    "security2_mortgagee2": "Text238",             # 2nd Mortgage – Lender Name
    "security2_debt1": "Text239",                  # 1st Mortgage – Amount ($)
    "security2_debt2": "Text240",                  # 2nd Mortgage – Amount ($)
    "security2_current_value": "Text243",          # Est. Current Value – Value ($)
    "security2_purchase_price": "Text244",         # Purchase Price – Value ($)
    "security2_type_other": "Text251",             # If Other, specify
    "security2_bedrooms": "Text252",               # No. of Bedrooms
    "security2_bathrooms": "Text253",              # No. of Bathrooms
    "security2_car_spaces": "Text254",             # No. of Car Spaces
    "security2_building_size": "Text255",          # Building Size (sqm)
    "security2_land_size": "Text256",              # Land Size (sqm)
    
    # SECTION 7: LOAN PURPOSES
    "loan_purpose1_desc": "Text263",               # Loan Purpose 1 → Description
    "loan_purpose1_amount": "Text264",             # Loan Purpose 1 → Amount ($)
    "loan_purpose2_desc": "Text265",               # Loan Purpose 2 → Description
    "loan_purpose2_amount": "Text266",             # Loan Purpose 2 → Amount ($)
    "loan_purpose3_desc": "Text267",               # Loan Purpose 3 → Description
    "loan_purpose3_amount": "Text268",             # Loan Purpose 3 → Amount ($)
    "loan_purpose4_desc": "Text269",               # Loan Purpose 4 → Description
    "loan_purpose4_amount": "Text270",             # Loan Purpose 4 → Amount ($)
    "loan_purpose5_desc": "Text271",               # Loan Purpose 5 → Description
    "loan_purpose5_amount": "Text272",             # Loan Purpose 5 → Amount ($)
    "loan_purpose6_desc": "Text273",               # Loan Purpose 6 → Description
    "loan_purpose6_amount": "Text274",             # Loan Purpose 6 → Amount ($)
    "loan_purposes_total": "Text275",              # Total ($)
}


# CHECKBOX FIELD MAPPINGS - Based on actual PDF checkbox field names
CHECKBOX_MAP: Dict[str, str] = {
    # Trustee status checkboxes
    "is_trustee_yes": "Check Box1",
    "is_trustee_no": "Check Box2",
    "is_smsf_trustee_yes": "Check Box3",
    "is_smsf_trustee_no": "Check Box4",
    
    # Director 1 roles
    "director1_role_director": "Check Box5",
    "director1_role_secretary": "Check Box6",
    "director1_role_public_officer": "Check Box7",
    
    # Director 2 roles
    "director2_role_director": "Check Box8",
    "director2_role_secretary": "Check Box9",
    "director2_role_public_officer": "Check Box10",
    
    # Employment types for individual borrowers/guarantors
    "borrower1_fulltime": "Check Box11",
    "borrower1_parttime": "Check Box12",
    "borrower1_casual": "Check Box13",
    "borrower1_contract": "Check Box14",
    
    "borrower2_fulltime": "Check Box15",
    "borrower2_parttime": "Check Box16",
    "borrower2_casual": "Check Box17",
    "borrower2_contract": "Check Box18",
    
    # Solvency enquiries checkboxes
    "pending_litigation_yes": "Check Box19",
    "pending_litigation_no": "Check Box20",
    "unsatisfied_judgements_yes": "Check Box21",
    "unsatisfied_judgements_no": "Check Box22",
    "been_bankrupt_yes": "Check Box23",
    "been_bankrupt_no": "Check Box24",
    "refused_credit_yes": "Check Box25",
    "refused_credit_no": "Check Box26",
    "ato_debt_yes": "Check Box27",
    "ato_debt_no": "Check Box28",
    "tax_returns_yes": "Check Box29",
    "tax_returns_no": "Check Box30",
    "payment_arrangements_yes": "Check Box31",
    "payment_arrangements_no": "Check Box32",
    
    # Property type checkboxes for security properties
    "security1_residential": "Check Box33",
    "security1_commercial": "Check Box34",
    "security1_rural": "Check Box35",
    "security1_industrial": "Check Box36",
    "security1_vacant_land": "Check Box37",
    "security1_other": "Check Box38",
    
    "security2_residential": "Check Box39",
    "security2_commercial": "Check Box40",
    "security2_rural": "Check Box41",
    "security2_industrial": "Check Box42",
    "security2_vacant_land": "Check Box43",
    "security2_other": "Check Box44",
    
    # Property structure checkboxes
    "security1_single_story": "Check Box45",
    "security1_double_story": "Check Box46",
    "security1_garage": "Check Box47",
    "security1_carport": "Check Box48",
    "security1_off_street": "Check Box49",
    
    "security2_single_story": "Check Box50",
    "security2_double_story": "Check Box51",
    "security2_garage": "Check Box52",
    "security2_carport": "Check Box53",
    "security2_off_street": "Check Box54",
}


# PDF PROCESSING CONFIGURATION
PDF_CONFIG = {
    'max_properties': 3,
    'max_loan_requirements': 6,
    'max_borrowers': 2,
    'max_guarantors': 2,
    'max_directors': 2,
    'max_company_assets': 4,
    'date_format': '%d/%m/%Y',
    'number_format': '%.2f',
}


# ERROR MESSAGES
ERROR_MESSAGES = {
    'pdf_not_found': 'PDF template file not found',
    'pdf_read_error': 'Error reading PDF file',
    'pdf_write_error': 'Error writing PDF file',
    'invalid_application': 'Invalid application data',
    'missing_data': 'Required data missing for PDF generation',
    'field_mapping_error': 'Error mapping application data to PDF fields',
}


# SUCCESS MESSAGES
SUCCESS_MESSAGES = {
    'pdf_generated': 'PDF successfully generated',
    'data_extracted': 'Application data successfully extracted',
    'form_filled': 'PDF form successfully filled',
} 