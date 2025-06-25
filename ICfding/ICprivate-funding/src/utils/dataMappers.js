/**
 * Data Mapping Utilities
 * 
 * This file contains utility functions to map data between frontend components
 * and backend API endpoints, ensuring proper field mapping and data transformation.
 * 
 * UNIFIED FIELD STRUCTURE:
 * Both Borrower and Guarantor models now use the same field definitions for:
 * - Personal Information (title, first_name, last_name, date_of_birth, drivers_licence_no, home_phone, mobile, email)
 * - Residential Address (address_unit, address_street_no, address_street_name, address_suburb, address_state, address_postcode)
 * - Employment Details (occupation, employer_name, employment_type, annual_income)
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
  // Create a new object with properly mapped fields using unified structure
  const apiData = {
    // ===== SHARED PERSONAL INFORMATION FIELDS =====
    title: formData.title || null,
    first_name: formData.first_name || "",
    last_name: formData.last_name || "",
    date_of_birth: formatDateForApi(formData.date_of_birth),
    drivers_licence_no: formData.drivers_licence_no || "",
    home_phone: formData.home_phone || "",
    mobile: formData.mobile || "",
    email: formData.email || "",
    
    // ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
    address_unit: formData.address_unit || "",
    address_street_no: formData.address_street_no || "",
    address_street_name: formData.address_street_name || "",
    address_suburb: formData.address_suburb || "",
    address_state: formData.address_state || "",
    address_postcode: formData.address_postcode || "",
    
    // ===== SHARED EMPLOYMENT DETAILS FIELDS =====
    occupation: formData.occupation || "",
    employer_name: formData.employer_name || "",
    employment_type: formData.employment_type || "",
    annual_income: formData.annual_income || null,
    
    // ===== BORROWER-SPECIFIC FIELDS =====
    tax_id: formData.tax_id || "",
    marital_status: formData.marital_status || "",
    residency_status: formData.residency_status || "",
    referral_source: formData.referral_source || "",
    tags: formData.tags || "",
    
    // Legacy fields for backward compatibility
    phone: formData.phone || formData.mobile || "",
    residential_address: formData.residential_address || "",
    mailing_address: formData.mailing_address || "",
    job_title: formData.job_title || formData.occupation || "",
    employment_duration: formData.employment_duration || null,
    employer_address: formData.employer_address || "",
    other_income: formData.other_income || null,
    monthly_expenses: formData.monthly_expenses || null,
    credit_score: formData.credit_score || null,
  };

  // Handle legacy address fields - combine into residential_address if new fields are not used
  if (!apiData.address_street_name && formData.address_street) {
    const addressParts = [];
    if (formData.address_street) addressParts.push(formData.address_street);
    if (formData.address_city) addressParts.push(formData.address_city);
    if (formData.address_state) addressParts.push(formData.address_state);
    if (formData.address_postal_code) addressParts.push(formData.address_postal_code);
    if (formData.address_country) addressParts.push(formData.address_country);
    
    if (addressParts.length > 0) {
      apiData.residential_address = addressParts.join(', ');
    }
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
    // ===== SHARED PERSONAL INFORMATION FIELDS =====
    title: apiData.title || "",
    first_name: apiData.first_name || "",
    last_name: apiData.last_name || "",
    date_of_birth: apiData.date_of_birth || "",
    drivers_licence_no: apiData.drivers_licence_no || "",
    home_phone: apiData.home_phone || "",
    mobile: apiData.mobile || "",
    email: apiData.email || "",
    
    // ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
    address_unit: apiData.address_unit || "",
    address_street_no: apiData.address_street_no || "",
    address_street_name: apiData.address_street_name || "",
    address_suburb: apiData.address_suburb || "",
    address_state: apiData.address_state || "",
    address_postcode: apiData.address_postcode || "",
    
    // ===== SHARED EMPLOYMENT DETAILS FIELDS =====
    occupation: apiData.occupation || "",
    employer_name: apiData.employer_name || "",
    employment_type: apiData.employment_type || "",
    annual_income: apiData.annual_income || null,
    
    // ===== BORROWER-SPECIFIC FIELDS =====
    tax_id: apiData.tax_id || "",
    marital_status: apiData.marital_status || "",
    residency_status: apiData.residency_status || "",
    referral_source: apiData.referral_source || "",
    tags: apiData.tags || "",
    
    // Legacy fields for backward compatibility
    phone: apiData.phone || apiData.mobile || "",
    residential_address: apiData.residential_address || "",
    mailing_address: apiData.mailing_address || "",
    job_title: apiData.job_title || apiData.occupation || "",
    employment_duration: apiData.employment_duration || null,
    employer_address: apiData.employer_address || "",
    other_income: apiData.other_income || null,
    monthly_expenses: apiData.monthly_expenses || null,
    credit_score: apiData.credit_score || null,
  };

  // Handle legacy address fields - parse residential_address if new fields are not available
  if (!apiData.address_street_name && apiData.residential_address) {
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

  return formData;
};

/**
 * Maps guarantor data from frontend form to backend API format
 * @param {Object} formData - The form data from the frontend
 * @returns {Object} - Data formatted for the backend API
 */
export const mapGuarantorFormToApi = (formData) => {
  // Create a new object with properly mapped fields using unified structure
  const apiData = {
    // ===== GUARANTOR-SPECIFIC FIELDS =====
    guarantor_type: formData.guarantor_type || "individual",
    
    // ===== SHARED PERSONAL INFORMATION FIELDS =====
    title: formData.title || null,
    first_name: formData.first_name || "",
    last_name: formData.last_name || "",
    date_of_birth: formatDateForApi(formData.date_of_birth),
    drivers_licence_no: formData.drivers_licence_no || "",
    home_phone: formData.home_phone || "",
    mobile: formData.mobile || "",
    email: formData.email || "",
    
    // ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
    address_unit: formData.address_unit || "",
    address_street_no: formData.address_street_no || "",
    address_street_name: formData.address_street_name || "",
    address_suburb: formData.address_suburb || "",
    address_state: formData.address_state || "",
    address_postcode: formData.address_postcode || "",
    
    // ===== SHARED EMPLOYMENT DETAILS FIELDS =====
    occupation: formData.occupation || "",
    employer_name: formData.employer_name || "",
    employment_type: formData.employment_type || "",
    annual_income: formData.annual_income || null,
    
    // ===== RELATIONSHIP FIELDS =====
    borrower: formData.borrower_id ? parseInt(formData.borrower_id) : null,
    application: formData.application_id ? parseInt(formData.application_id) : null,
  };

  // Map company fields if it's a company guarantor
  if (formData.guarantor_type === 'company') {
    apiData.company_name = formData.company_name || "";
    apiData.company_abn = formData.company_abn || "";
    apiData.company_acn = formData.company_acn || "";
  }

  // Legacy field mapping for backward compatibility
  if (formData.phone && !formData.mobile) {
    apiData.mobile = formData.phone;
  }
  if (formData.mobile && !formData.mobile) {
    apiData.mobile = formData.mobile;
  }
  if (formData.home_phone && !formData.home_phone) {
    apiData.home_phone = formData.home_phone;
  }

  // Legacy address field mapping
  if (formData.address && !formData.address_street_name) {
    apiData.address_street_name = formData.address;
  }
  if (formData.city && !formData.address_suburb) {
    apiData.address_suburb = formData.city;
  }
  if (formData.postal_code && !formData.address_postcode) {
    apiData.address_postcode = formData.postal_code;
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
    // ===== GUARANTOR-SPECIFIC FIELDS =====
    guarantor_type: apiData.guarantor_type || "individual",
    
    // ===== SHARED PERSONAL INFORMATION FIELDS =====
    title: apiData.title || "",
    first_name: apiData.first_name || "",
    last_name: apiData.last_name || "",
    date_of_birth: apiData.date_of_birth || "",
    drivers_licence_no: apiData.drivers_licence_no || "",
    home_phone: apiData.home_phone || "",
    mobile: apiData.mobile || "",
    email: apiData.email || "",
    
    // ===== SHARED RESIDENTIAL ADDRESS FIELDS =====
    address_unit: apiData.address_unit || "",
    address_street_no: apiData.address_street_no || "",
    address_street_name: apiData.address_street_name || "",
    address_suburb: apiData.address_suburb || "",
    address_state: apiData.address_state || "",
    address_postcode: apiData.address_postcode || "",
    
    // ===== SHARED EMPLOYMENT DETAILS FIELDS =====
    occupation: apiData.occupation || "",
    employer_name: apiData.employer_name || "",
    employment_type: apiData.employment_type || "",
    annual_income: apiData.annual_income || null,
    
    // ===== RELATIONSHIP FIELDS =====
    borrower_id: apiData.borrower ? parseInt(apiData.borrower) : null,
    application_id: apiData.application ? parseInt(apiData.application) : null,
    relationship: apiData.relationship || "",
  };

  // Map company fields if it's a company guarantor
  if (apiData.guarantor_type === 'company') {
    formData.company_name = apiData.company_name || "";
    formData.company_abn = apiData.company_abn || "";
    formData.company_acn = apiData.company_acn || "";
  }

  // Legacy field mapping for backward compatibility
  formData.phone = apiData.mobile || apiData.mobile || "";
  formData.mobile = apiData.mobile || apiData.mobile || "";
  formData.home_phone = apiData.home_phone || "";
  
  // Legacy address field mapping
  formData.address = apiData.address_street_name || "";
  formData.city = apiData.address_suburb || "";
  formData.state = apiData.address_state || "";
  formData.postal_code = apiData.address_postcode || "";

  return formData;
};
