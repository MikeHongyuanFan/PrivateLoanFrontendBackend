# Unified Field Structure Implementation

## Overview

This document outlines the unified field structure implementation for individual borrowers and guarantors in the Vue.js frontend application. The goal is to ensure both entity types use the exact same fields for personal information, residential address, and employment details, while maintaining separate components for better user experience.

## ✅ **Components with Correct Unified Field Structure**

### 1. Application Creation/Edit Components
- **`guarantor.vue` (addapplication)** - ✅ **CORRECT**
- **`inividual.vue` (addapplication)** - ✅ **CORRECT**
- **`addborrower.vue`** - ✅ **CORRECT**
- **`addguarantor.vue`** - ✅ **CORRECT**
- **`EditApplication.vue`** - ✅ **CORRECT**

### 2. Display Components
- **`application.vue`** - ✅ **CORRECT** (uses cascade data)
- **`ApplicationTable.vue`** - ✅ **CORRECT** (summary data only)
- **`ArchivedApplications.vue`** - ✅ **CORRECT** (listing only)

### 3. Updated View Components
- **`borrower.vue` (view)** - ✅ **UPDATED** (now uses unified fields)
- **`guarantor.vue` (view)** - ✅ **UPDATED** (now uses unified fields)

## Unified Field Structure

### Shared Personal Information Fields
Both individual borrowers and guarantors now use these exact same fields:

```javascript
// Personal Information
title: "",                    // mr, mrs, ms, miss, dr, other
first_name: "",              // Required
last_name: "",               // Required
date_of_birth: "",           // YYYY-MM-DD format
drivers_licence_no: "",      // Optional
phone_home: "",              // Home phone number
phone_mobile: "",            // Mobile phone number
email: "",                   // Required
```

### Shared Residential Address Fields
Both entity types use the same structured address fields:

```javascript
// Residential Address
unit_no: "",                 // Unit, apartment, suite number
street_no: "",               // Street number
street_name: "",             // Street name
suburb: "",                  // Suburb or city
state: "",                   // NSW, VIC, QLD, WA, SA, TAS, ACT, NT
postcode: "",                // 4-digit postcode
```

### Shared Employment Details Fields
Both entity types use the same employment information:

```javascript
// Employment Details
occupation: "",              // Job title or occupation
employer_name: "",           // Current employer name
employment_type: "",         // full_time, part_time, casual, contract
annual_income: null,         // Annual income amount
```

### Entity-Specific Fields

#### Individual Borrower Only
```javascript
// Borrower-specific fields
tax_id: "",                  // Tax File Number
marital_status: "",          // single, married, de_facto, divorced, widowed
residency_status: "",        // citizen, permanent_resident, temporary_resident, foreign_investor
referral_source: "",         // How they heard about us
tags: "",                    // Any tags or notes
```

#### Guarantor Only
```javascript
// Guarantor-specific fields
guarantor_type: "individual", // individual or company
borrower: null,              // Related borrower ID
application: null,           // Related application ID

// Company guarantor fields (when guarantor_type === 'company')
company_name: "",            // Company name
company_abn: "",             // Australian Business Number
company_acn: "",             // Australian Company Number
```

## Data Mapping Implementation

### Backend to Frontend Mapping
The `dataMappers.js` utility provides functions to map between API and form formats:

```javascript
// For borrowers
mapBorrowerApiToForm(apiData)    // Converts API response to form format
mapBorrowerFormToApi(formData)    // Converts form data to API format

// For guarantors
mapGuarantorApiToForm(apiData)   // Converts API response to form format
mapGuarantorFormToApi(formData)  // Converts form data to API format
```

### Backward Compatibility
All components maintain backward compatibility with legacy fields:

```javascript
// Legacy fields (still supported for existing data)
phone: "",                    // Legacy single phone field
residential_address: "",      // Legacy address field
mailing_address: "",          // Legacy mailing address
job_title: "",               // Legacy job title
employment_duration: null,    // Legacy employment duration
employer_address: "",        // Legacy employer address
other_income: null,          // Legacy other income
monthly_expenses: null,      // Legacy monthly expenses
credit_score: null,          // Legacy credit score
```

## Component Updates Summary

### ✅ Updated Components

1. **`borrower.vue` (view)**
   - Added unified personal information fields (title, drivers_licence_no, phone_home, phone_mobile)
   - Added unified residential address fields (unit_no, street_no, street_name, suburb, state, postcode)
   - Added unified employment fields (occupation)
   - Moved legacy fields to separate "Legacy Information" tab
   - Added formatting functions for new fields

2. **`guarantor.vue` (view)**
   - Added unified personal information fields (title, drivers_licence_no, phone_home, phone_mobile)
   - Added unified residential address fields (unit_no, street_no, street_name, suburb, state, postcode)
   - Added unified employment fields (occupation)
   - Added company details section for company guarantors
   - Moved legacy fields to separate "Legacy Information" tab
   - Added formatting functions for new fields

### ✅ Already Correct Components

3. **`guarantor.vue` (addapplication)**
   - Uses all unified fields correctly
   - Proper field validation and structure

4. **`inividual.vue` (addapplication)**
   - Uses all unified fields correctly
   - Proper field validation and structure

5. **`addborrower.vue`**
   - Uses data mappers for proper field conversion
   - Maintains backward compatibility

6. **`addguarantor.vue`**
   - Uses data mappers for proper field conversion
   - Maintains backward compatibility

7. **`EditApplication.vue`**
   - Uses unified fields for both borrowers and guarantors
   - Proper data transformation and validation

8. **`application.vue`**
   - Uses cascade data properly
   - No direct field access needed

9. **`ApplicationTable.vue`**
   - Only displays summary data
   - No direct field access needed

10. **`ArchivedApplications.vue`**
    - Only handles application listing
    - No direct field access needed

## Field Validation

### Required Fields
- **Individual Borrowers**: `first_name`, `last_name`, `email`
- **Guarantors**: `first_name`, `last_name`, `email`, `guarantor_type`
- **Company Guarantors**: `company_name`, `company_abn`

### Optional Fields
All other fields are optional and can be left empty.

## Data Type Handling

### Numeric Fields
- `annual_income`: Converted to number/null for API
- `bedrooms`, `bathrooms`, `car_spaces`: Converted to integers/null
- Legacy numeric fields: Maintained for backward compatibility

### Boolean Fields
- `has_garage`, `has_carport`, `is_single_story`, `has_off_street_parking`: Converted to boolean/null

### Date Fields
- `date_of_birth`: YYYY-MM-DD format
- All dates properly formatted for display

## Migration Strategy

### Phase 1: ✅ Complete
- Updated backend models and serializers
- Created and applied database migrations
- Updated frontend form components
- Updated data mappers

### Phase 2: ✅ Complete
- Updated view components for display
- Added backward compatibility
- Added proper field formatting
- Added validation and error handling

### Phase 3: ✅ Complete
- Testing and validation
- Documentation updates
- Performance optimization

## Benefits Achieved

1. **Consistency**: Both borrowers and guarantors now use identical field structures
2. **Maintainability**: Single source of truth for field definitions
3. **User Experience**: Consistent form layouts and validation
4. **Data Integrity**: Proper field validation and type conversion
5. **Backward Compatibility**: Existing data continues to work
6. **Future-Proofing**: Easy to add new shared fields

## Testing Guidelines

### Form Testing
- Test all unified fields in both borrower and guarantor forms
- Verify data mapping between frontend and backend
- Test validation for required fields
- Test optional field handling

### Display Testing
- Verify all unified fields display correctly in view components
- Test formatting functions for various field values
- Verify legacy field fallbacks work properly

### API Testing
- Test create/update operations with unified fields
- Verify backward compatibility with legacy data
- Test cascade operations with new field structure

## Notes for Developers

1. **Always use data mappers** when converting between API and form formats
2. **Maintain backward compatibility** when adding new fields
3. **Use proper field validation** for required fields
4. **Format display values** using the provided formatting functions
5. **Test both individual and company guarantors** when making changes
6. **Update documentation** when adding new shared fields

## Future Enhancements

1. **Additional Shared Fields**: Consider adding more shared fields as needed
2. **Enhanced Validation**: Add more sophisticated field validation
3. **Field Dependencies**: Implement conditional field display based on entity type
4. **Bulk Operations**: Support bulk updates with unified field structure
5. **Reporting**: Enhanced reporting capabilities with unified data structure 