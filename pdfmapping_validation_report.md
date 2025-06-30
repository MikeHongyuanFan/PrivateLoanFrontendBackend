# PDF Field Mapping Validation Report

## Executive Summary

This report validates the database field paths in the PDF mapping document against the actual backend Django models. The validation reveals several issues that need to be addressed:

- **1 Critical Missing Field**: `second_mortgagee` field is missing from SecurityProperty model
- **Multiple Incorrect Field Paths**: Several mappings reference non-existent or incorrectly named fields
- **Relationship Structure Issues**: Some mappings don't account for the actual relationship structure
- **Field Type Mismatches**: Some fields exist but with different names or types

## Detailed Validation Results

### ✅ **CORRECT MAPPINGS**

#### Application Core Fields
| PDF Field ID | Database Field Path | Status | Notes |
|--------------|-------------------|---------|-------|
| Text297 | `application.loan_amount` | ✅ Correct | |
| Text298 | `application.loan_term` | ✅ Correct | |
| Text299-301 | `application.estimated_settlement_date` | ✅ Correct | |
| Text302 | `application.interest_rate` | ✅ Correct | |
| Text312 | `application.additional_comments` | ✅ Correct | |
| Text315 | `application.other_credit_providers_details` | ✅ Correct | |
| Text333 | `application.exit_strategy_details` | ✅ Correct | |

#### Solvency Enquiries
| PDF Field ID | Database Field Path | Status | Notes |
|--------------|-------------------|---------|-------|
| Check Box92/93 | `application.has_pending_litigation` | ✅ Correct | |
| Check Box94/95 | `application.has_unsatisfied_judgements` | ✅ Correct | |
| Check Box96/97 | `application.has_been_bankrupt` | ✅ Correct | |
| Check Box98/99 | `application.has_been_refused_credit` | ✅ Correct | |
| Check Box100/101 | `application.has_outstanding_ato_debt` | ✅ Correct | |
| Check Box102/103 | `application.has_outstanding_tax_returns` | ✅ Correct | |
| Check Box104/105 | `application.has_payment_arrangements` | ✅ Correct | |

#### Loan Requirements
| PDF Field ID | Database Field Path | Status | Notes |
|--------------|-------------------|---------|-------|
| Text316/317 | `application.loan_requirements[0].description/amount` | ✅ Correct | |
| Text318/319 | `application.loan_requirements[1].description/amount` | ✅ Correct | |
| Text320/321 | `application.loan_requirements[2].description/amount` | ✅ Correct | |
| Text322/323 | `application.loan_requirements[3].description/amount` | ✅ Correct | |
| Text324/325 | `application.loan_requirements[4].description/amount` | ✅ Correct | |
| Text326/327 | `application.loan_requirements[5].description/amount` | ✅ Correct | |

#### Security Properties
| PDF Field ID | Database Field Path | Status | Notes |
|--------------|-------------------|---------|-------|
| Text198/231/264 | `application.security_properties[index].address_unit` | ✅ Correct | |
| Text199/232/265 | `application.security_properties[index].address_street_no` | ✅ Correct | |
| Text200/233/266 | `application.security_properties[index].address_street_name` | ✅ Correct | |
| Text201/234/267 | `application.security_properties[index].address_suburb` | ✅ Correct | |
| Text202/235/268 | `application.security_properties[index].address_state` | ✅ Correct | |
| Text203/236/269 | `application.security_properties[index].address_postcode` | ✅ Correct | |
| Text206/239/272 | `application.security_properties[index].first_mortgage_debt` | ✅ Correct | |
| Text207/240/273 | `application.security_properties[index].second_mortgage_debt` | ✅ Correct | |
| Text210/242/276 | `application.security_properties[index].estimated_value` | ✅ Correct | |
| Text211/244/277 | `application.security_properties[index].purchase_price` | ✅ Correct | |
| Text219/252/285 | `application.security_properties[index].bedrooms` | ✅ Correct | |
| Text220/253/286 | `application.security_properties[index].bathrooms` | ✅ Correct | |
| Text221/254/287 | `application.security_properties[index].car_spaces` | ✅ Correct | |
| Text222/255/288 | `application.security_properties[index].building_size` | ✅ Correct | |
| Text223/256/289 | `application.security_properties[index].land_size` | ✅ Correct | |
| Text224/257/290 | `application.security_properties[index].is_single_story` | ✅ Correct | |
| Text226/259/292 | `application.security_properties[index].has_garage` | ✅ Correct | |
| Text227/260/293 | `application.security_properties[index].has_carport` | ✅ Correct | |
| Text228/261/294 | `application.security_properties[index].has_off_street_parking` | ✅ Correct | |
| Text229/262/295 | `application.security_properties[index].occupancy` | ✅ Correct | |

### ❌ **INCORRECT MAPPINGS**

#### Critical Missing Field
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| **Text205/238/271** | `application.security_properties[index].second_mortgagee` | ❌ **MISSING** | **CRITICAL**: `second_mortgagee` field does not exist in SecurityProperty model |

#### Company Borrower Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text1 | `application.company_borrowers.company_name` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].company_name` |
| Text2 | `application.company_borrowers.company_abn / company_acn` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].company_abn` |
| Text3 | `application.company_borrowers.industry_type` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].industry_type` |
| Text4 | `application.company_borrowers.contact_number` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].contact_number` |
| Text5 | `application.company_borrowers.annual_company_income` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].annual_company_income` |
| Check Box20/21 | `application.company_borrowers.is_trustee` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].is_trustee` |
| Check Box22/23 | `application.company_borrowers.is_smsf_trustee` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].is_smsf_trustee` |
| Text6 | `application.company_borrowers.trustee_name` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].trustee_name` |

#### Company Directors Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text7 | `application.company_borrowers.directors[0].name` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].directors[0].name` |
| Check Box24/25/26 | `application.company_borrowers.directors[0].roles` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].directors[0].roles` |
| Text8–Text19 | `application.company_borrowers.directors[0].director_id` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].directors[0].director_id` |

#### Company Registered Address Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text43 | `application.company_borrowers.registered_address_unit` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_unit` |
| Text44 | `application.company_borrowers.registered_address_street_no` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_street_no` |
| Text45 | `application.company_borrowers.registered_address_street_name` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_street_name` |
| Text46 | `application.company_borrowers.registered_address_suburb` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_suburb` |
| Text47 | `application.company_borrowers.registered_address_state` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_state` |
| Text48 | `application.company_borrowers.registered_address_postcode` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].registered_address_postcode` |

#### Company Assets Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text49 | `application.company_borrowers.assets[0].address` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].assets[0].address` |
| Text50 | `application.company_borrowers.assets[0].value` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].assets[0].value` |
| Text51 | `application.company_borrowers.assets[0].amount_owing` | ❌ Incorrect | Should be `application.borrowers.filter(is_company=True)[index].assets[0].amount_owing` |

#### Individual Borrower/Guarantor Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text106 | `application.borrowers[0].title OR application.guarantors[0].title` | ❌ Incorrect | Should be `application.borrowers[0].title` or `application.guarantors[0].title` (separate paths) |
| Text107 | `application.borrowers[0].first_name OR application.guarantors[0].first_name` | ❌ Incorrect | Should be `application.borrowers[0].first_name` or `application.guarantors[0].first_name` (separate paths) |
| Text108 | `application.borrowers[0].last_name OR application.guarantors[0].last_name` | ❌ Incorrect | Should be `application.borrowers[0].last_name` or `application.guarantors[0].last_name` (separate paths) |

#### Security Property Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Text204/237/270 | `application.security_properties[index].current_mortgagee` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].current_mortgagee` |
| Check Box212/245/278 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Check Box213/246/279 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Check Box214/247/280 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Check Box215/248/281 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Check Box216/249/282 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Check Box217/250/283 | `application.security_properties[index].property_type` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].property_type` |
| Text218/251/284 | `application.security_properties[index].description_if_applicable` | ❌ Incorrect | Field exists but mapping should be `application.security_properties[index].description_if_applicable` |

#### Loan Purpose Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Check Box303-311 | `application.loan_purpose` | ❌ Incorrect | Field exists but mapping should be `application.loan_purpose` |

#### Exit Strategy Issues
| PDF Field ID | Database Field Path | Status | Issue |
|--------------|-------------------|---------|-------|
| Check Box329-332 | `application.exit_strategy` | ❌ Incorrect | Field exists but mapping should be `application.exit_strategy` |

### ⚠️ **FIELDS NOT IN CURRENT SCHEMA (CALCULATED)**

| PDF Field ID | Database Field Path | Status | Notes |
|--------------|-------------------|---------|-------|
| Text77 | ❌ Not in current schema (calculated) | ⚠️ Calculated | Total Value of Assets ($) - needs calculation |
| Text78 | ❌ Not in current schema (calculated) | ⚠️ Calculated | Total Amount Owing ($) - needs calculation |
| Text178 | ❌ Not in current schema (calculated) | ⚠️ Calculated | Total Value of All Assets ($) - needs calculation |
| Text179 | ❌ Not in current schema (calculated) | ⚠️ Calculated | Total Amount Owing on All Assets ($) - needs calculation |
| Text328 | ❌ Not in current schema (calculated) | ⚠️ Calculated | Total Amount ($) of All Loan Purposes - needs calculation |

### 🔧 **REQUIRED FIXES**

#### 1. **CRITICAL: Add Missing Field to SecurityProperty Model**

```python
# In applications/models/properties.py
class SecurityProperty(BaseApplicationModel):
    # ... existing fields ...
    
    second_mortgagee = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Second mortgage holder"
    )
```

#### 2. **Fix Company Borrower Field Paths**

All company borrower fields should use the pattern:
```
application.borrowers.filter(is_company=True)[index].field_name
```

Instead of:
```
application.company_borrowers.field_name
```

#### 3. **Fix Individual Borrower/Guarantor Field Paths**

Separate the OR conditions into distinct paths:
- For borrowers: `application.borrowers[index].field_name`
- For guarantors: `application.guarantors[index].field_name`

#### 4. **Add Calculated Field Methods**

Add methods to calculate totals:
```python
# In Application model
@property
def total_assets_value(self):
    """Calculate total value of all assets across all borrowers and guarantors"""
    # Implementation needed

@property
def total_assets_owing(self):
    """Calculate total amount owing on all assets"""
    # Implementation needed

@property
def total_loan_requirements_amount(self):
    """Calculate total amount of all loan requirements"""
    # Implementation needed
```

## Recommendations

1. **Immediate Action**: Add the missing `second_mortgagee` field to SecurityProperty model
2. **Update Mapping Document**: Correct all field paths to match actual database schema
3. **Implement Calculated Fields**: Add methods to calculate totals for assets and loan requirements
4. **Test Validation**: Verify all field paths work correctly with actual data
5. **Documentation Update**: Update the mapping document with corrected field paths

## Conclusion

The mapping document has significant discrepancies with the actual backend schema. The most critical issue is the missing `second_mortgagee` field, but there are also numerous field path corrections needed. The backend uses a unified Borrower model for both individual and company borrowers, with an `is_company` flag to distinguish between them, which the mapping document doesn't properly reflect. 