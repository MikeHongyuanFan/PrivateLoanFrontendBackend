/**
 * Data Mapping Utilities
 * 
 * This file contains utility functions to map data between frontend components
 * and backend API endpoints, ensuring proper field mapping and data transformation.
 */

/**
 * Formats a date object or string to YYYY-MM-DD format for API
 * @param {Date|string} dateValue - The date to format
 * @returns {string|null} - Formatted date string or null if invalid
 */
const formatDateForApi = (dateValue) => {
  if (!dateValue) return null;
  
  try {
    let date;
    if (dateValue instanceof Date) {
      date = dateValue;
    } else if (typeof dateValue === 'string') {
      // If it's already in YYYY-MM-DD format, return it
      if (/^\d{4}-\d{2}-\d{2}$/.test(dateValue)) {
        return dateValue;
      }
      date = new Date(dateValue);
    } else {
      return null;
    }
    
    // Check if date is valid
    if (isNaN(date.getTime())) {
      return null;
    }
    
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  } catch (e) {
    console.error('Error formatting date:', e);
    return null;
  }
};

/**
 * Maps borrower data from frontend form to backend API format
 * @param {Object} formData - The form data from the frontend
 * @returns {Object} - Data formatted for the backend API
 */
export const mapBorrowerFormToApi = (formData) => {
  // Create a new object with properly mapped fields
  const apiData = {
    first_name: formData.first_name || "",
    last_name: formData.last_name || "",
    email: formData.email || "",
    phone: formData.phone || "",
    date_of_birth: formatDateForApi(formData.date_of_birth),
    tax_id: formData.tax_id || "",
    marital_status: formData.marital_status || "",
    residency_status: formData.residency_status || "",
    referral_source: formData.referral_source || "",
    tags: formData.tags || "",
    employment_type: formData.employment_type || "",
    
    // Employment fields
    employer_name: formData.employer_name || "",
    job_title: formData.job_title || "",
    annual_income: formData.annual_income || null,
    employment_duration: formData.employment_duration || null,
    employer_address: formData.employer_address || "",
    
    // Financial fields
    other_income: formData.other_income || null,
    monthly_expenses: formData.monthly_expenses || null,
    credit_score: formData.credit_score || null,
  };

  // Handle address fields - combine into residential_address
  const addressParts = [];
  if (formData.address_street) addressParts.push(formData.address_street);
  if (formData.address_city) addressParts.push(formData.address_city);
  if (formData.address_state) addressParts.push(formData.address_state);
  if (formData.address_postal_code) addressParts.push(formData.address_postal_code);
  if (formData.address_country) addressParts.push(formData.address_country);
  
  if (addressParts.length > 0) {
    apiData.residential_address = addressParts.join(', ');
  }

  // Handle mailing address
  if (formData.mailing_address) {
    apiData.mailing_address = formData.mailing_address;
  }

  return apiData;
};

/**
 * Maps borrower data from backend API to frontend form format
 * @param {Object} apiData - The data from the backend API
 * @returns {Object} - Data formatted for the frontend form
 */
export const mapBorrowerApiToForm = (apiData) => {
  const formData = {
    first_name: apiData.first_name || "",
    last_name: apiData.last_name || "",
    email: apiData.email || "",
    phone: apiData.phone || "",
    date_of_birth: apiData.date_of_birth || "",
    tax_id: apiData.tax_id || "",
    marital_status: apiData.marital_status || "",
    residency_status: apiData.residency_status || "",
    referral_source: apiData.referral_source || "",
    tags: apiData.tags || "",
    employment_type: apiData.employment_type || "",
    
    // Employment fields
    employer_name: apiData.employer_name || "",
    job_title: apiData.job_title || "",
    annual_income: apiData.annual_income || null,
    employment_duration: apiData.employment_duration || null,
    employer_address: apiData.employer_address || "",
    
    // Financial fields
    other_income: apiData.other_income || null,
    monthly_expenses: apiData.monthly_expenses || null,
    credit_score: apiData.credit_score || null,
  };

  // Handle address fields - parse residential_address if it exists
  if (apiData.residential_address) {
    const addressParts = apiData.residential_address.split(', ').map(part => part.trim());
    formData.address_street = addressParts[0] || "";
    formData.address_city = addressParts[1] || "";
    formData.address_state = addressParts[2] || "";
    formData.address_postal_code = addressParts[3] || "";
    formData.address_country = addressParts[4] || "";
  } else {
    formData.address_street = "";
    formData.address_city = "";
    formData.address_state = "";
    formData.address_postal_code = "";
    formData.address_country = "";
  }

  // Handle mailing address
  formData.mailing_address = apiData.mailing_address || "";

  return formData;
};

/**
 * Maps guarantor data from frontend form to backend API format
 * @param {Object} formData - The form data from the frontend
 * @returns {Object} - Data formatted for the backend API
 */
export const mapGuarantorFormToApi = (formData) => {
  // Create a new object with properly mapped fields
  const apiData = {
    guarantor_type: formData.guarantor_type || "individual",
    first_name: formData.first_name || "",
    last_name: formData.last_name || "",
    email: formData.email || "",
    mobile: formData.phone || "", // Map phone to mobile
    date_of_birth: formatDateForApi(formData.date_of_birth)
  };

  // Map address fields - use the correct field names from the backend model
  if (formData.address) {
    apiData.address_street_name = formData.address;
  }
  if (formData.city) {
    apiData.address_suburb = formData.city;
  }
  if (formData.state) {
    apiData.address_state = formData.state;
  }
  if (formData.postal_code) {
    apiData.address_postcode = formData.postal_code;
  }

  // Map employment fields
  if (formData.employment_type) {
    apiData.employment_type = formData.employment_type;
  }
  if (formData.employer_name) {
    apiData.employer_name = formData.employer_name;
  }
  if (formData.annual_income) {
    apiData.annual_income = formData.annual_income;
  }
  if (formData.years_with_employer) {
    apiData.employment_duration = formData.years_with_employer * 12; // Convert years to months
  }

  // Map relationship fields - ensure they are properly set
  if (formData.borrower_id) {
    apiData.borrower = parseInt(formData.borrower_id);
  }
  if (formData.application_id) {
    apiData.application = parseInt(formData.application_id);
  }

  // Map company fields if it's a company guarantor
  if (formData.guarantor_type === 'company') {
    apiData.company_name = formData.company_name || "";
    apiData.company_abn = formData.company_abn || "";
    apiData.company_acn = formData.company_acn || "";
  }

  return apiData;
};

/**
 * Maps guarantor data from backend API to frontend form format
 * @param {Object} apiData - The data from the backend API
 * @returns {Object} - Data formatted for the frontend form
 */
export const mapGuarantorApiToForm = (apiData) => {
  const formData = {
    guarantor_type: apiData.guarantor_type || "individual",
    first_name: apiData.first_name || "",
    last_name: apiData.last_name || "",
    date_of_birth: apiData.date_of_birth || "",
    email: apiData.email || "",
    phone: apiData.mobile || "", // Map mobile to phone
    employment_type: apiData.employment_type || "",
    employer_name: apiData.employer_name || "",
    annual_income: apiData.annual_income || null,
    relationship: apiData.relationship || "",
  };

  // Map address fields
  formData.address = apiData.address_street_name || "";
  formData.city = apiData.address_suburb || "";
  formData.state = apiData.address_state || "";
  formData.postal_code = apiData.address_postcode || "";

  // Map relationship fields
  if (apiData.borrower) {
    formData.borrower_id = parseInt(apiData.borrower);
  }
  if (apiData.application) {
    formData.application_id = parseInt(apiData.application);
  }

  // Map company fields if it's a company guarantor
  if (apiData.guarantor_type === 'company') {
    formData.company_name = apiData.company_name || "";
    formData.company_abn = apiData.company_abn || "";
    formData.company_acn = apiData.company_acn || "";
  }

  return formData;
};
