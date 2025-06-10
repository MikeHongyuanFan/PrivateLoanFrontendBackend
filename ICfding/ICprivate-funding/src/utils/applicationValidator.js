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
  
  // Validate required top-level fields
  if (!applicationData.loan_amount) {
    errors.loan_amount = 'Loan amount is required';
  }
  
  if (!applicationData.loan_term) {
    errors.loan_term = 'Loan term is required';
  }
  
  if (!applicationData.repayment_frequency) {
    errors.repayment_frequency = 'Repayment frequency is required';
  }
  
  if (!applicationData.stage) {
    errors.stage = 'Application stage is required';
  }

  if (!applicationData.application_type) {
    errors.application_type = 'Application type is required';
  }
  
  // Validate borrowers if present
  if (applicationData.borrowers && applicationData.borrowers.length > 0) {
    const borrowerErrors = [];
    
    applicationData.borrowers.forEach((borrower, index) => {
      const borrowerFieldErrors = {};
      
      // Check for required borrower fields
      if (!borrower.first_name) {
        borrowerFieldErrors.first_name = 'First name is required';
      }
      
      if (!borrower.last_name) {
        borrowerFieldErrors.last_name = 'Last name is required';
      }

      if (!borrower.email) {
        borrowerFieldErrors.email = 'Email is required';
      }
      
      if (Object.keys(borrowerFieldErrors).length > 0) {
        borrowerErrors[index] = borrowerFieldErrors;
      }
    });
    
    if (borrowerErrors.length > 0) {
      errors.borrowers = borrowerErrors;
    }
  }
  
  // Validate company borrowers if present
  if (applicationData.company_borrowers && applicationData.company_borrowers.length > 0) {
    const companyBorrowerErrors = [];
    
    applicationData.company_borrowers.forEach((companyBorrower, index) => {
      const companyBorrowerFieldErrors = {};
      
      if (!companyBorrower.company_name) {
        companyBorrowerFieldErrors.company_name = 'Company name is required';
      }
      
      if (!companyBorrower.company_abn && !companyBorrower.company_acn) {
        companyBorrowerFieldErrors.company_identification = 'Either ABN or ACN is required';
      }

      if (!companyBorrower.industry_type) {
        companyBorrowerFieldErrors.industry_type = 'Industry type is required';
      }

      if (!companyBorrower.contact_number) {
        companyBorrowerFieldErrors.contact_number = 'Contact number is required';
      }
      
      // Validate directors if present
      if (companyBorrower.directors && companyBorrower.directors.length > 0) {
        const directorErrors = [];
        
        companyBorrower.directors.forEach((director, dirIndex) => {
          const directorFieldErrors = {};
          
          if (!director.name) {
            directorFieldErrors.name = 'Director name is required';
          }
          
          if (!director.roles) {
            directorFieldErrors.roles = 'Director roles are required';
          }
          
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
  
  // Validate guarantors if present
  if (applicationData.guarantors && applicationData.guarantors.length > 0) {
    const guarantorErrors = [];
    
    applicationData.guarantors.forEach((guarantor, index) => {
      const guarantorFieldErrors = {};
      
      if (!guarantor.guarantor_type) {
        guarantorFieldErrors.guarantor_type = 'Guarantor type is required';
      }
      
      if (!guarantor.first_name) {
        guarantorFieldErrors.first_name = 'First name is required';
      }
      
      if (!guarantor.last_name) {
        guarantorFieldErrors.last_name = 'Last name is required';
      }

      if (!guarantor.email) {
        guarantorFieldErrors.email = 'Email is required';
      }

      if (!guarantor.mobile) {
        guarantorFieldErrors.mobile = 'Mobile number is required';
      }
      
      // Validate guarantor assets if present
      if (guarantor.assets && guarantor.assets.length > 0) {
        const assetErrors = [];
        
        guarantor.assets.forEach((asset, assetIndex) => {
          const assetFieldErrors = {};
          
          if (!asset.asset_type) {
            assetFieldErrors.asset_type = 'Asset type is required';
          }
          
          if (!asset.bg_type) {
            assetFieldErrors.bg_type = 'BG type is required for guarantor assets';
          }

          if (!asset.value) {
            assetFieldErrors.value = 'Asset value is required';
          }
          
          if (Object.keys(assetFieldErrors).length > 0) {
            assetErrors[assetIndex] = assetFieldErrors;
          }
        });
        
        if (assetErrors.length > 0) {
          guarantorFieldErrors.assets = assetErrors;
        }
      }

      // Validate guarantor liabilities if present
      if (guarantor.liabilities && guarantor.liabilities.length > 0) {
        const liabilityErrors = [];
        
        guarantor.liabilities.forEach((liability, liabilityIndex) => {
          const liabilityFieldErrors = {};
          
          if (!liability.liability_type) {
            liabilityFieldErrors.liability_type = 'Liability type is required';
          }
          
          if (!liability.description) {
            liabilityFieldErrors.description = 'Description is required';
          }

          if (!liability.amount) {
            liabilityFieldErrors.amount = 'Amount is required';
          }

          if (!liability.bg_type) {
            liabilityFieldErrors.bg_type = 'BG type is required';
          }
          
          if (Object.keys(liabilityFieldErrors).length > 0) {
            liabilityErrors[liabilityIndex] = liabilityFieldErrors;
          }
        });
        
        if (liabilityErrors.length > 0) {
          guarantorFieldErrors.liabilities = liabilityErrors;
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
  
  // Validate security properties if present
  if (applicationData.security_properties && applicationData.security_properties.length > 0) {
    const propertyErrors = [];
    
    applicationData.security_properties.forEach((property, index) => {
      const propertyFieldErrors = {};
      
      // Check for required address fields
      const addressFields = [
        { field: 'address_street_no', label: 'Street number' },
        { field: 'address_street_name', label: 'Street name' },
        { field: 'address_suburb', label: 'Suburb' },
        { field: 'address_state', label: 'State' },
        { field: 'address_postcode', label: 'Postcode' }
      ];
      
      addressFields.forEach(({ field, label }) => {
        if (!property[field]) {
          propertyFieldErrors[field] = `${label} is required`;
        }
      });

      if (!property.property_type) {
        propertyFieldErrors.property_type = 'Property type is required';
      }

      if (!property.estimated_value) {
        propertyFieldErrors.estimated_value = 'Estimated value is required';
      }
      
      if (Object.keys(propertyFieldErrors).length > 0) {
        propertyErrors[index] = propertyFieldErrors;
      }
    });
    
    if (propertyErrors.length > 0) {
      errors.security_properties = propertyErrors;
    }
  }

  // Validate loan requirements if present
  if (applicationData.loan_requirements && applicationData.loan_requirements.length > 0) {
    const requirementErrors = [];
    
    applicationData.loan_requirements.forEach((requirement, index) => {
      const requirementFieldErrors = {};
      
      if (!requirement.description) {
        requirementFieldErrors.description = 'Description is required';
      }
      
      if (!requirement.amount) {
        requirementFieldErrors.amount = 'Amount is required';
      }
      
      if (Object.keys(requirementFieldErrors).length > 0) {
        requirementErrors[index] = requirementFieldErrors;
      }
    });
    
    if (requirementErrors.length > 0) {
      errors.loan_requirements = requirementErrors;
    }
  }

  // Validate funding calculation input if present
  if (applicationData.funding_calculation_input) {
    const fundingErrors = {};
    const input = applicationData.funding_calculation_input;
    
    if (!input.establishment_fee_rate) {
      fundingErrors.establishment_fee_rate = 'Establishment fee rate is required';
    }
    
    if (!input.monthly_line_fee_rate) {
      fundingErrors.monthly_line_fee_rate = 'Monthly line fee rate is required';
    }
    
    if (!input.brokerage_fee_rate) {
      fundingErrors.brokerage_fee_rate = 'Brokerage fee rate is required';
    }
    
    if (!input.application_fee) {
      fundingErrors.application_fee = 'Application fee is required';
    }
    
    if (!input.due_diligence_fee) {
      fundingErrors.due_diligence_fee = 'Due diligence fee is required';
    }
    
    if (!input.legal_fee_before_gst) {
      fundingErrors.legal_fee_before_gst = 'Legal fee is required';
    }
    
    if (!input.valuation_fee) {
      fundingErrors.valuation_fee = 'Valuation fee is required';
    }
    
    if (!input.monthly_account_fee) {
      fundingErrors.monthly_account_fee = 'Monthly account fee is required';
    }
    
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