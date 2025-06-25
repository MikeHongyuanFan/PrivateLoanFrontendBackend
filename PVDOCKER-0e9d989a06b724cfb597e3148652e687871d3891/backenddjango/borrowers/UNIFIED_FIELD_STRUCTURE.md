# Unified Field Structure: Borrower and Guarantor Models

## 🎯 Overview

This document outlines the unified field structure implemented between the `Borrower` and `Guarantor` models to ensure consistency, prevent confusion, and support shared frontend components while maintaining separate entities.

## 📋 Shared Field Definitions

Both `Borrower` and `Guarantor` models now use the exact same field definitions for individual information, residential address, and employment details.

### 👤 Personal Information Fields

| Field Name | Type | Max Length | Choices | Description |
|------------|------|------------|---------|-------------|
| `title` | CharField | 10 | mr, mrs, ms, miss, dr, other | Person's title |
| `first_name` | CharField | 100 | - | Person's first name |
| `last_name` | CharField | 100 | - | Person's last name |
| `date_of_birth` | DateField | - | - | Person's date of birth |
| `drivers_licence_no` | CharField | 50 | - | Driver's license number |
| `home_phone` | CharField | 20 | - | Home phone number |
| `mobile` | CharField | 20 | - | Mobile phone number |
| `email` | EmailField | - | - | Email address |

### 🏠 Residential Address Fields

| Field Name | Type | Max Length | Description |
|------------|------|------------|-------------|
| `address_unit` | CharField | 20 | Unit/apartment number |
| `address_street_no` | CharField | 20 | Street number |
| `address_street_name` | CharField | 100 | Street name |
| `address_suburb` | CharField | 100 | Suburb/town |
| `address_state` | CharField | 50 | State/territory |
| `address_postcode` | CharField | 10 | Postal code |

### 💼 Employment Details Fields

| Field Name | Type | Max Length | Choices | Description |
|------------|------|------------|---------|-------------|
| `occupation` | CharField | 100 | - | Job title/occupation |
| `employer_name` | CharField | 255 | - | Employer company name |
| `employment_type` | CharField | 20 | full_time, part_time, casual, self_employed, contractor, unemployed, retired | Employment type |
| `annual_income` | DecimalField | 12,2 | - | Annual income amount |

## 🔄 Field Mapping for Frontend Components

### Shared Form Fields

When building frontend components for both borrowers and guarantors, use these consistent field names:

```javascript
// Personal Information
const personalFields = {
  title: '',
  first_name: '',
  last_name: '',
  date_of_birth: '',
  drivers_licence_no: '',
  home_phone: '',
  mobile: '',
  email: ''
};

// Residential Address
const addressFields = {
  address_unit: '',
  address_street_no: '',
  address_street_name: '',
  address_suburb: '',
  address_state: '',
  address_postcode: ''
};

// Employment Details
const employmentFields = {
  occupation: '',
  employer_name: '',
  employment_type: '',
  annual_income: ''
};
```

### API Endpoints

Both models use the same field structure in their respective API endpoints:

- **Borrowers**: `/api/borrowers/`
- **Guarantors**: `/api/guarantors/`

### Serializer Field Names

The serializers (`BorrowerDetailSerializer` and `GuarantorSerializer`) use identical field names for the shared fields, ensuring consistent API responses.

## 🏗️ Model-Specific Fields

### Borrower-Specific Fields

Borrowers have additional fields not shared with guarantors:

- **Identity**: `tax_id`, `marital_status`, `residency_status`
- **Financial**: `other_income`, `monthly_expenses`
- **Banking**: `bank_name`, `bank_account_name`, `bank_account_number`, `bank_bsb`
- **Company**: `is_company`, `company_name`, `company_abn`, `company_acn`, etc.
- **Metadata**: `referral_source`, `tags`, `notes_text`

### Guarantor-Specific Fields

Guarantors have additional fields not shared with borrowers:

- **Type**: `guarantor_type` (individual/company)
- **Company**: `company_name`, `company_abn`, `company_acn` (for company guarantors)
- **Relationships**: `borrower`, `application`

## 🔄 Legacy Field Migration

### Deprecated Fields

The following legacy fields are kept for backward compatibility but should not be used in new code:

#### Borrower Legacy Fields:
- `phone` → Use `home_phone` or `mobile` instead
- `residential_address` → Use structured address fields instead
- `mailing_address` → Use structured address fields instead
- `job_title` → Use `occupation` instead
- `employer_address` → Legacy field
- `employment_duration` → Legacy field

#### Guarantor Legacy Fields:
- `address` → Use structured address fields instead

### Migration Guidance

If you have existing data using legacy fields, consider migrating to the new unified structure:

```python
# Example migration for phone field
if borrower.phone:
    borrower.home_phone = borrower.phone
    borrower.save()

# Example migration for address field
if borrower.residential_address:
    # Parse the text address and populate structured fields
    # This would require address parsing logic
    pass
```

## 🎨 Frontend Implementation Guidelines

### 1. Shared Components

Create reusable form components that work for both borrowers and guarantors:

```vue
<!-- PersonalInformationForm.vue -->
<template>
  <div class="personal-info-form">
    <select v-model="formData.title">
      <option value="mr">Mr</option>
      <option value="mrs">Mrs</option>
      <option value="ms">Ms</option>
      <option value="miss">Miss</option>
      <option value="dr">Dr</option>
      <option value="other">Other</option>
    </select>
    
    <input v-model="formData.first_name" placeholder="First Name" />
    <input v-model="formData.last_name" placeholder="Last Name" />
    <input v-model="formData.date_of_birth" type="date" />
    <input v-model="formData.drivers_licence_no" placeholder="Driver's License" />
    <input v-model="formData.home_phone" placeholder="Home Phone" />
    <input v-model="formData.mobile" placeholder="Mobile" />
    <input v-model="formData.email" type="email" placeholder="Email" />
  </div>
</template>

<script>
export default {
  props: {
    modelValue: {
      type: Object,
      default: () => ({
        title: '',
        first_name: '',
        last_name: '',
        date_of_birth: '',
        drivers_licence_no: '',
        home_phone: '',
        mobile: '',
        email: ''
      })
    }
  },
  emits: ['update:modelValue'],
  computed: {
    formData: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    }
  }
}
</script>
```

### 2. Address Component

```vue
<!-- AddressForm.vue -->
<template>
  <div class="address-form">
    <input v-model="formData.address_unit" placeholder="Unit" />
    <input v-model="formData.address_street_no" placeholder="Street No" />
    <input v-model="formData.address_street_name" placeholder="Street Name" />
    <input v-model="formData.address_suburb" placeholder="Suburb" />
    <input v-model="formData.address_state" placeholder="State" />
    <input v-model="formData.address_postcode" placeholder="Postcode" />
  </div>
</template>
```

### 3. Employment Component

```vue
<!-- EmploymentForm.vue -->
<template>
  <div class="employment-form">
    <input v-model="formData.occupation" placeholder="Occupation" />
    <input v-model="formData.employer_name" placeholder="Employer Name" />
    <select v-model="formData.employment_type">
      <option value="full_time">Full Time</option>
      <option value="part_time">Part Time</option>
      <option value="casual">Casual</option>
      <option value="self_employed">Self Employed</option>
      <option value="contractor">Contractor</option>
      <option value="unemployed">Unemployed</option>
      <option value="retired">Retired</option>
    </select>
    <input v-model="formData.annual_income" type="number" placeholder="Annual Income" />
  </div>
</template>
```

## 🔧 API Usage Examples

### Creating a Borrower

```javascript
const borrowerData = {
  // Shared fields
  title: 'mr',
  first_name: 'John',
  last_name: 'Doe',
  date_of_birth: '1990-01-01',
  drivers_licence_no: '123456789',
  home_phone: '02 1234 5678',
  mobile: '0412 345 678',
  email: 'john.doe@example.com',
  
  // Address fields
  address_unit: '1A',
  address_street_no: '123',
  address_street_name: 'Main Street',
  address_suburb: 'Sydney',
  address_state: 'NSW',
  address_postcode: '2000',
  
  // Employment fields
  occupation: 'Software Engineer',
  employer_name: 'Tech Corp',
  employment_type: 'full_time',
  annual_income: '80000.00',
  
  // Borrower-specific fields
  tax_id: '123456789',
  marital_status: 'single',
  residency_status: 'citizen'
};

// POST to /api/borrowers/
const response = await fetch('/api/borrowers/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(borrowerData)
});
```

### Creating a Guarantor

```javascript
const guarantorData = {
  // Shared fields (same structure as borrower)
  title: 'mrs',
  first_name: 'Jane',
  last_name: 'Smith',
  date_of_birth: '1985-05-15',
  drivers_licence_no: '987654321',
  home_phone: '02 9876 5432',
  mobile: '0498 765 432',
  email: 'jane.smith@example.com',
  
  // Address fields (same structure as borrower)
  address_unit: '2B',
  address_street_no: '456',
  address_street_name: 'Oak Avenue',
  address_suburb: 'Melbourne',
  address_state: 'VIC',
  address_postcode: '3000',
  
  // Employment fields (same structure as borrower)
  occupation: 'Accountant',
  employer_name: 'Finance Ltd',
  employment_type: 'full_time',
  annual_income: '75000.00',
  
  // Guarantor-specific fields
  guarantor_type: 'individual'
};

// POST to /api/guarantors/
const response = await fetch('/api/guarantors/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(guarantorData)
});
```

## ✅ Benefits of Unified Structure

1. **Consistency**: Both models use identical field names and types
2. **Reusability**: Frontend components can be shared between borrowers and guarantors
3. **Maintainability**: Changes to shared fields only need to be made once
4. **API Consistency**: Same field names across different endpoints
5. **Data Integrity**: Reduced risk of field mapping errors
6. **Developer Experience**: Clear, predictable field structure

## 🚀 Next Steps

1. **Update Frontend Components**: Modify existing borrower and guarantor forms to use the new unified field structure
2. **Data Migration**: Consider migrating existing data from legacy fields to new structured fields
3. **Testing**: Ensure all API endpoints work correctly with the new field structure
4. **Documentation**: Update API documentation to reflect the unified structure

## 📞 Support

For questions or issues related to the unified field structure, please refer to:
- Backend team for model and API changes
- Frontend team for component updates
- Database team for migration assistance 