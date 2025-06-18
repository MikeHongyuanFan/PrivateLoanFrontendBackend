/**
 * Utility functions to validate application data before sending to the backend
 */

/**
 * Validates an application payload for the create-with-cascade endpoint
 * @param {Object} applicationData - The application data to validate
 * @returns {Object} - Object with isValid boolean and errors object
 */
export function validateApplicationPayload(applicationData) {
  const errors = {};
  
  // All fields are now optional - only validate format/type when values are provided
  
  // Validate borrowers format if present
  if (applicationData.borrowers && applicationData.borrowers.length > 0) {
    const borrowerErrors = [];
    
    applicationData.borrowers.forEach((borrower, index) => {
      const borrowerFieldErrors = {};
      
      // Only validate email format if provided
      if (borrower.email && borrower.email.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(borrower.email)) {
          borrowerFieldErrors.email = 'Please enter a valid email address';
        }
      }
      
      if (Object.keys(borrowerFieldErrors).length > 0) {
        borrowerErrors[index] = borrowerFieldErrors;
      }
    });
    
    if (borrowerErrors.length > 0) {
      errors.borrowers = borrowerErrors;
    }
  }
  
  // Validate company borrowers format if present
  if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
    const companyBorrowerErrors = [];
    
    applicationData.company_borrowers.forEach((companyBorrower, index) => {
      const companyBorrowerFieldErrors = {};
      
      // Validate directors format if present
      if (companyBorrower.directors && companyBorrower.directors.length > 0) {
        const directorErrors = [];
        
        companyBorrower.directors.forEach((director, dirIndex) => {
          const directorFieldErrors = {};
          
          // No required validations - all optional
          
          if (Object.keys(directorFieldErrors).length > 0) {
            directorErrors[dirIndex] = directorFieldErrors;
          }
        });
        
        if (directorErrors.length > 0) {
          companyBorrowerFieldErrors.directors = directorErrors;
        }
      }
      
      if (Object.keys(companyBorrowerFieldErrors).length > 0) {
        companyBorrowerErrors[index] = companyBorrowerFieldErrors;
      }
    });
    
    if (companyBorrowerErrors.length > 0) {
      errors.company_borrowers = companyBorrowerErrors;
    }
  }
  
  // Validate guarantors format if present
  if (applicationData.guarantors && applicationData.guarantors.length > 0) {
    const guarantorErrors = [];
    
    applicationData.guarantors.forEach((guarantor, index) => {
      const guarantorFieldErrors = {};
      
      // Validate email format if provided
      if (guarantor.email && guarantor.email.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(guarantor.email)) {
          guarantorFieldErrors.email = 'Please enter a valid email address';
        }
      }
      
      if (Object.keys(guarantorFieldErrors).length > 0) {
        guarantorErrors[index] = guarantorFieldErrors;
      }
    });
    
    if (guarantorErrors.length > 0) {
      errors.guarantors = guarantorErrors;
    }
  }
  
  // Validate security properties format if present
  if (applicationData.security_properties && applicationData.security_properties.length > 0) {
    const propertyErrors = [];
    
    applicationData.security_properties.forEach((property, index) => {
      const propertyFieldErrors = {};
      
      // Validate numeric fields format if provided
      if (property.estimated_value && isNaN(parseFloat(property.estimated_value))) {
        propertyFieldErrors.estimated_value = 'Please enter a valid number';
      }
      
      if (property.purchase_price && isNaN(parseFloat(property.purchase_price))) {
        propertyFieldErrors.purchase_price = 'Please enter a valid number';
      }
      
      if (Object.keys(propertyFieldErrors).length > 0) {
        propertyErrors[index] = propertyFieldErrors;
      }
    });
    
    if (propertyErrors.length > 0) {
      errors.security_properties = propertyErrors;
    }
  }

  // Validate loan requirements format if present
  if (applicationData.loan_requirements && applicationData.loan_requirements.length > 0) {
    const requirementErrors = [];
    
    applicationData.loan_requirements.forEach((requirement, index) => {
      const requirementFieldErrors = {};
      
      // Validate amount format if provided
      if (requirement.amount && isNaN(parseFloat(requirement.amount))) {
        requirementFieldErrors.amount = 'Please enter a valid number';
      }
      
      if (Object.keys(requirementFieldErrors).length > 0) {
        requirementErrors[index] = requirementFieldErrors;
      }
    });
    
    if (requirementErrors.length > 0) {
      errors.loan_requirements = requirementErrors;
    }
  }

  // Validate funding calculation input format if present
  if (applicationData.funding_calculation_input) {
    const fundingErrors = {};
    const input = applicationData.funding_calculation_input;
    
    // Validate numeric formats if provided
    const numericFields = [
      'establishment_fee_rate', 'monthly_line_fee_rate', 'brokerage_fee_rate',
      'application_fee', 'due_diligence_fee', 'legal_fee_before_gst',
      'valuation_fee', 'monthly_account_fee'
    ];
    
    numericFields.forEach(field => {
      if (input[field] && isNaN(parseFloat(input[field]))) {
        fundingErrors[field] = 'Please enter a valid number';
      }
    });
    
    if (Object.keys(fundingErrors).length > 0) {
      errors.funding_calculation_input = fundingErrors;
    }
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

/**
 * Formats validation errors from the backend into a more user-friendly format
 * @param {Object} backendErrors - The errors object from the backend
 * @returns {Object} - Formatted errors object
 */
export function formatBackendErrors(backendErrors) {
  if (!backendErrors) return {};
  
  const formattedErrors = {};
  
  // Process top-level errors
  Object.keys(backendErrors).forEach(key => {
    if (Array.isArray(backendErrors[key])) {
      // Handle array of strings
      if (typeof backendErrors[key][0] === 'string') {
        formattedErrors[key] = backendErrors[key].join(', ');
      } 
      // Handle array of objects (nested errors)
      else if (typeof backendErrors[key][0] === 'object') {
        formattedErrors[key] = backendErrors[key].map(item => {
          if (typeof item === 'object') {
            // Process each nested object
            const nestedErrors = {};
            Object.keys(item).forEach(nestedKey => {
              if (Array.isArray(item[nestedKey])) {
                nestedErrors[nestedKey] = item[nestedKey].join(', ');
              } else if (typeof item[nestedKey] === 'object') {
                // Handle doubly nested objects (like assets)
                nestedErrors[nestedKey] = formatBackendErrors(item[nestedKey]);
              } else {
                nestedErrors[nestedKey] = item[nestedKey];
              }
            });
            return nestedErrors;
          }
          return item;
        });
      }
    } else if (typeof backendErrors[key] === 'object' && !Array.isArray(backendErrors[key])) {
      // Handle nested objects
      formattedErrors[key] = formatBackendErrors(backendErrors[key]);
    } else {
      formattedErrors[key] = backendErrors[key];
    }
  });
  
  // Special handling for company_borrowers to map company_identification errors
  if (formattedErrors.company_borrowers && Array.isArray(formattedErrors.company_borrowers)) {
    formattedErrors.company_borrowers = formattedErrors.company_borrowers.map(companyBorrower => {
      // If there's a company_identification error, make sure it's properly formatted
      if (companyBorrower && companyBorrower.company_identification) {
        const error = companyBorrower.company_identification;
        if (Array.isArray(error)) {
          companyBorrower.company_identification = error.join(', ');
        }
      }
      return companyBorrower;
    });
  }
  
  return formattedErrors;
}

/**
 * Creates a sample application payload with all required fields
 * @returns {Object} - A sample application payload
 */
export function createSampleApplicationPayload() {
  return {
    loan_amount: "500000.00",
    loan_term: 24,
    interest_rate: "5.5",
    repayment_frequency: "monthly",
    stage: "inquiry",
    purpose: "Investment property purchase",
    application_type: "residential",
    loan_purpose: "purchase",
    borrowers: [
      {
        first_name: "John",
        last_name: "Doe",
        email: "john.doe@example.com",
        phone: "0412345678",
        date_of_birth: "1980-01-01"
      }
    ],
    guarantors: [
      {
        guarantor_type: "individual",
        first_name: "Jane",
        last_name: "Smith",
        email: "jane.smith@example.com",
        mobile: "0412345679",
        date_of_birth: "1982-02-02",
        assets: [
          {
            asset_type: "Property",
            description: "Investment property",
            value: "750000.00",
            bg_type: "BG1"
          }
        ],
        liabilities: [
          {
            liability_type: "mortgage",
            description: "Home loan",
            amount: "400000.00",
            monthly_payment: "2500.00",
            bg_type: "bg1"
          }
        ]
      }
    ],
    company_borrowers: [
      {
        company_name: "Example Pty Ltd",
        company_abn: "12345678901",
        company_acn: "123456789",
        industry_type: "real_estate",
        contact_number: "0298765432",
        directors: [
          {
            name: "John Director",
            roles: "Director, Secretary",
            director_id: "DIR123"
          }
        ]
      }
    ],
    security_properties: [
      {
        address_unit: "",
        address_street_no: "123",
        address_street_name: "Main Street",
        address_suburb: "Sydney",
        address_state: "NSW",
        address_postcode: "2000",
        property_type: "house",
        estimated_value: "750000.00"
      }
    ],
    loan_requirements: [
      {
        description: "Property purchase",
        amount: "500000.00"
      }
    ],
    funding_calculation_input: {
      establishment_fee_rate: "2.5",
      capped_interest_months: 9,
      monthly_line_fee_rate: "0.25",
      brokerage_fee_rate: "1.0",
      application_fee: "500.00",
      due_diligence_fee: "1000.00",
      legal_fee_before_gst: "2000.00",
      valuation_fee: "800.00",
      monthly_account_fee: "50.00",
      working_fee: "0.00"
    }
  };
}