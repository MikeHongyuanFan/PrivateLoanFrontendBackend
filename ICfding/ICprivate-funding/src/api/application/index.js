import sendRequest from "@/server/sendRequest";

export function applications(params) {
    return sendRequest({
        url: "/api/applications/applications/enhanced_list/",
        method: "get",
        params: params,
    });
}
export function addApplications(params) {
    return sendRequest({
        url: "/api/applications/create-with-cascade/",
        method: "post",
        data: params,
    });
}
export function application(params) {
    console.log("=== API APPLICATION FUNCTION DEBUG ===");
    console.log("API call: application() with params:", params);
    console.log("Params type:", typeof params);
    console.log("Params value:", params);
    console.log("Params constructor:", params?.constructor?.name);
    
    // Validate the params parameter
    if (!params || typeof params === 'object' && params.constructor?.name === 'PointerEvent') {
        console.error("❌ Invalid params passed to application function:", params);
        console.error("Params details:", {
            value: params,
            type: typeof params,
            constructor: params?.constructor?.name,
            isPointerEvent: params?.constructor?.name === 'PointerEvent'
        });
        return Promise.resolve([{ detail: 'Invalid application ID' }, null]);
    }
    
    console.log("✅ Valid params, making API request for:", params);
    return sendRequest({
        url: `/api/applications/applications/${params}/`,
        method: "get",
    }).then(([err, res]) => {
        if (err) {
            console.error("API Error in application():", err);
            return [err, null];
        } else {
            console.log("API Success in application(), response:", res);
            
            // Ensure all expected fields are present with defaults
            if (res) {
                // Ensure guarantors array exists
                res.guarantors = res.guarantors || [];
                
                // Ensure each guarantor has assets and liabilities (from unified tables)
                res.guarantors.forEach(guarantor => {
                    guarantor.assets = guarantor.assets || [];      // From unified Asset table
                    guarantor.liabilities = guarantor.liabilities || [];  // From unified Liability table
                });
                
                // Ensure borrowers array exists
                res.borrowers = res.borrowers || [];
                
                // Ensure borrowers have assets and liabilities (from unified tables)
                res.borrowers.forEach(borrower => {
                    borrower.assets = borrower.assets || [];        // From unified Asset table
                    borrower.liabilities = borrower.liabilities || [];    // From unified Liability table
                });
                
                // Ensure security_properties array exists
                res.security_properties = res.security_properties || [];
                
                // Ensure loan_requirements array exists
                res.loan_requirements = res.loan_requirements || [];
                
                // Ensure documents, notes, fees, repayments arrays exist
                res.documents = res.documents || [];
                res.notes = res.notes || [];
                res.fees = res.fees || [];
                res.repayments = res.repayments || [];
                res.ledger_entries = res.ledger_entries || [];
                res.funding_calculation_history = res.funding_calculation_history || [];
            }
            
            return [null, res];
        }
    });
}
export function calculator(params) {
    return sendRequest({
        url: `/api/applications/manual-funding-calculator/`,
        method: "post",
        data: params,
    });
}
export function notes() {
    return sendRequest({
        url: `/api/documents/notes/`,
        method: "get",
    });
}
export function addNote(params) {
    return sendRequest({
        url: `/api/documents/notes/`,
        method: "post",
        data: params,
    });
}
export function updateStage(id, params) {
    return sendRequest({
        url: `/api/applications/${id}/stage/`,
        method: "put",
        data: params,
    });
}

/**
 * Creates an application with all related entities (borrowers, guarantors, etc.)
 * @param {Object} params - The application data
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function createApplicationWithCascade(params) {
    return sendRequest({
        url: "/api/applications/create-with-cascade/",
        method: "post",
        data: params,
    }).catch(error => {
        // Handle any unexpected errors
        console.error("Error creating application with cascade:", error);
        
        const formattedErrors = error.response?.data?.errors || { general: "An unexpected error occurred" };
            
        return [
            { 
                status: error.response?.status || 500,
                detail: error.response?.data?.detail || "Server error",
                errors: formattedErrors
            }, 
            null
        ];
    });
}
export function deleteApplication(params) {
  return sendRequest({
    url: `/api/applications/applications/${params}`,
    method: 'delete',
  })
}

/**
 * Updates an existing application with all related entities
 * @param {number} id - The application ID
 * @param {Object} params - The updated application data
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function updateApplication(id, params) {
    console.log("API call: updateApplication() with id:", id);
    console.log("Update data:", params);
    
    return sendRequest({
        url: `/api/applications/applications/${id}/`,
        method: "put",
        data: params,
    }).then(([err, res]) => {
        if (err) {
            console.error("Error updating application:", err);
        } else {
            console.log("Application updated successfully:", res);
        }
        return [err, res];
    }).catch(error => {
        console.error("Exception in updateApplication:", error);
        const formattedErrors = error.response?.data?.errors || { general: "An unexpected error occurred" };
        return [
            { 
                status: error.response?.status || 500,
                detail: error.response?.data?.detail || "Server error",
                errors: formattedErrors
            }, 
            null
        ];
    });
}

/**
 * Updates an existing application with all related entities using partial update with cascade
 * @param {number} id - The application ID
 * @param {Object} params - The updated application data
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function updateApplicationWithCascade(id, params) {
    console.log("API call: updateApplicationWithCascade() with id:", id);
    console.log("Update data:", params);
    
    return sendRequest({
        url: `/api/applications/${id}/partial-update-cascade/`,
        method: "patch",
        data: params,
    }).then(([err, res]) => {
        if (err) {
            console.error("Error updating application with cascade:", err);
        } else {
            console.log("Application updated successfully with cascade:", res);
        }
        return [err, res];
    }).catch(error => {
        console.error("Exception in updateApplicationWithCascade:", error);
        const formattedErrors = error.response?.data?.errors || { general: "An unexpected error occurred" };
        return [
            { 
                status: error.response?.status || 500,
                detail: error.response?.data?.detail || "Server error",
                errors: formattedErrors
            }, 
            null
        ];
    });
}

export function generatePdf(params) {
    return sendRequest({
        url: `/api/applications/${params}/generate-pdf/`,
        method: 'get',
        responseType: 'blob'
    })
}
export function fees(params) {
    return sendRequest({
        url: `/api/documents/fees/`,
        method: 'get',
        params: params
    })
}
export function assignBd(params, data) {
    return sendRequest({
        url: `/api/applications/applications/${params}/assign_bd/`,
        method: 'put',
        data: data
    })
}

// Valuer API functions
export function valuers(params) {
    return sendRequest({
        url: '/api/applications/valuers/',
        method: 'get',
        params: params,
    });
}

export function addValuer(params) {
    return sendRequest({
        url: '/api/applications/valuers/',
        method: 'post',
        data: params,
    });
}

export function updateValuer(id, params) {
    return sendRequest({
        url: `/api/applications/valuers/${id}/`,
        method: 'put',
        data: params,
    });
}

export function deactivateValuer(id) {
    return sendRequest({
        url: `/api/applications/valuers/${id}/deactivate/`,
        method: 'post',
    });
}

export function activateValuer(id) {
    return sendRequest({
        url: `/api/applications/valuers/${id}/activate/`,
        method: 'post',
    });
}

// Quantity Surveyor API functions
export function quantitySurveyors(params) {
    return sendRequest({
        url: '/api/applications/quantity-surveyors/',
        method: 'get',
        params: params,
    });
}

export function addQuantitySurveyor(params) {
    return sendRequest({
        url: '/api/applications/quantity-surveyors/',
        method: 'post',
        data: params,
    });
}

export function updateQuantitySurveyor(id, params) {
    return sendRequest({
        url: `/api/applications/quantity-surveyors/${id}/`,
        method: 'put',
        data: params,
    });
}

export function deactivateQuantitySurveyor(id) {
    return sendRequest({
        url: `/api/applications/quantity-surveyors/${id}/deactivate/`,
        method: 'post',
    });
}

export function activateQuantitySurveyor(id) {
    return sendRequest({
        url: `/api/applications/quantity-surveyors/${id}/activate/`,
        method: 'post',
    });
}

/**
 * Retrieves an application with comprehensive cascade data including all related entities
 * @param {number} id - The application ID
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function applicationWithCascade(id) {
    console.log("=== API FUNCTION DEBUG ===");
    console.log("API call: applicationWithCascade() with id:", id);
    console.log("ID type:", typeof id);
    console.log("ID value:", id);
    console.log("ID constructor:", id?.constructor?.name);
    console.log("Is ID a number?", typeof id === 'number');
    console.log("Is ID a string?", typeof id === 'string');
    console.log("Is ID an object?", typeof id === 'object');
    
    // Validate the ID parameter
    if (!id || typeof id === 'object') {
        console.error("❌ Invalid ID passed to API function:", id);
        console.error("ID details:", {
            value: id,
            type: typeof id,
            constructor: id?.constructor?.name,
            isPointerEvent: id?.constructor?.name === 'PointerEvent'
        });
        return Promise.resolve([{ detail: 'Invalid application ID' }, null]);
    }
    
    console.log("✅ Valid ID, making API request for:", id);
    return sendRequest({
        url: `/api/applications/${id}/retrieve-cascade/`,
        method: "get",
    }).then(([err, res]) => {
        if (err) {
            console.error("API Error in applicationWithCascade():", err);
            return [err, null];
        } else {
            console.log("API Success in applicationWithCascade(), response:", res);
            
            // The cascade endpoint already provides comprehensive data, but ensure defaults
            if (res) {
                // Ensure all expected arrays exist with defaults
                res.borrowers = res.borrowers || [];
                res.company_borrowers = res.company_borrowers || []; // NEW: Separate company borrowers
                res.guarantors = res.guarantors || [];
                res.security_properties = res.security_properties || [];
                res.loan_requirements = res.loan_requirements || [];
                res.documents = res.documents || [];
                res.notes = res.notes || [];
                res.fees = res.fees || [];
                res.repayments = res.repayments || [];
                res.ledger_entries = res.ledger_entries || [];
                res.funding_calculation_history = res.funding_calculation_history || [];
                
                // Ensure individual borrowers have assets and liabilities (from unified tables)
                res.borrowers.forEach(borrower => {
                    borrower.assets = borrower.assets || [];        // From unified Asset table
                    borrower.liabilities = borrower.liabilities || [];    // From unified Liability table
                });
                
                // NEW: Ensure company borrowers have assets and liabilities with trust structure fields
                res.company_borrowers.forEach(company => {
                    company.assets = company.assets || [];        // From unified Asset table
                    company.liabilities = company.liabilities || [];    // From unified Liability table
                    
                    // Ensure trust structure fields are present
                    company.is_trustee = company.is_trustee || false;
                    company.is_smsf_trustee = company.is_smsf_trustee || false;
                    company.trustee_name = company.trustee_name || null;
                    
                    // Process company assets to handle updated asset types
                    company.assets.forEach(asset => {
                        // Remove "To be refinanced" asset type - convert to "Other" if needed
                        if (asset.asset_type === 'To be refinanced') {
                            asset.asset_type = 'Other';
                            if (!asset.description_if_applicable) {
                                asset.description_if_applicable = 'Originally "To be refinanced" asset';
                            }
                        }
                        
                        // Ensure to_be_refinanced field is present for company assets
                        asset.to_be_refinanced = asset.to_be_refinanced || false;
                        
                        // Remove bg_type for company assets (not applicable)
                        delete asset.bg_type;
                    });
                    
                    // Process company liabilities
                    company.liabilities.forEach(liability => {
                        // Ensure to_be_refinanced field is present for company liabilities
                        liability.to_be_refinanced = liability.to_be_refinanced || false;
                        
                        // Remove bg_type for company liabilities (not applicable)
                        delete liability.bg_type;
                    });
                });
                
                // Ensure guarantors have assets and liabilities (from unified tables - should already be there from cascade)
                res.guarantors.forEach(guarantor => {
                    guarantor.assets = guarantor.assets || [];      // From unified Asset table
                    guarantor.liabilities = guarantor.liabilities || [];  // From unified Liability table
                    
                    // Process guarantor assets to handle updated asset types
                    guarantor.assets.forEach(asset => {
                        // Remove "To be refinanced" asset type - convert to "Other" if needed
                        if (asset.asset_type === 'To be refinanced') {
                            asset.asset_type = 'Other';
                            if (!asset.description_if_applicable) {
                                asset.description_if_applicable = 'Originally "To be refinanced" asset';
                            }
                        }
                        
                        // Remove to_be_refinanced for guarantor assets (not applicable)
                        delete asset.to_be_refinanced;
                        
                        // Ensure bg_type is present for guarantor assets
                        asset.bg_type = asset.bg_type || 'BG1';
                    });
                    
                    // Process guarantor liabilities
                    guarantor.liabilities.forEach(liability => {
                        // Remove to_be_refinanced for guarantor liabilities (not applicable)
                        delete liability.to_be_refinanced;
                        
                        // Ensure bg_type is present for guarantor liabilities
                        liability.bg_type = liability.bg_type || 'bg1';
                    });
                });
                
                // Process individual borrower assets and liabilities
                res.borrowers.forEach(borrower => {
                    borrower.assets.forEach(asset => {
                        // Remove "To be refinanced" asset type - convert to "Other" if needed
                        if (asset.asset_type === 'To be refinanced') {
                            asset.asset_type = 'Other';
                            if (!asset.description_if_applicable) {
                                asset.description_if_applicable = 'Originally "To be refinanced" asset';
                            }
                        }
                        
                        // Remove to_be_refinanced for individual borrower assets (not applicable)
                        delete asset.to_be_refinanced;
                        delete asset.bg_type;
                    });
                    
                    borrower.liabilities.forEach(liability => {
                        // Remove to_be_refinanced for individual borrower liabilities (not applicable)
                        delete liability.to_be_refinanced;
                        delete liability.bg_type;
                    });
                });
                
                // Additional computed properties for easy access
                res.total_borrower_count = res.borrowers.length + res.company_borrowers.length;
                res.total_individual_borrower_count = res.borrowers.length;
                res.total_company_borrower_count = res.company_borrowers.length;
                res.total_guarantor_count = res.guarantors.length;
                res.total_security_property_count = res.security_properties.length;
                res.total_loan_requirement_count = res.loan_requirements.length;
                
                // Calculate total amounts
                res.total_loan_requirement_amount = res.loan_requirements.reduce((sum, req) => 
                    sum + (parseFloat(req.amount) || 0), 0);
                res.total_security_value = res.security_properties.reduce((sum, prop) => 
                    sum + (parseFloat(prop.estimated_value) || 0), 0);
                
                // Calculate individual borrower totals
                res.borrowers.forEach(borrower => {
                    borrower.total_assets = borrower.assets.reduce((sum, asset) => 
                        sum + (parseFloat(asset.value) || 0), 0);
                    borrower.total_liabilities = borrower.liabilities.reduce((sum, liability) => 
                        sum + (parseFloat(liability.amount) || 0), 0);
                    borrower.net_worth = borrower.total_assets - borrower.total_liabilities;
                });
                
                // Calculate company borrower totals
                res.company_borrowers.forEach(company => {
                    company.total_assets = company.assets.reduce((sum, asset) => 
                        sum + (parseFloat(asset.value) || 0), 0);
                    company.total_liabilities = company.liabilities.reduce((sum, liability) => 
                        sum + (parseFloat(liability.amount) || 0), 0);
                    company.net_worth = company.total_assets - company.total_liabilities;
                });
                
                // Calculate guarantor totals
                res.guarantors.forEach(guarantor => {
                    if (!guarantor.total_assets) {
                        guarantor.total_assets = guarantor.assets.reduce((sum, asset) => 
                            sum + (parseFloat(asset.value) || 0), 0);
                    }
                    if (!guarantor.total_liabilities) {
                        guarantor.total_liabilities = guarantor.liabilities.reduce((sum, liability) => 
                            sum + (parseFloat(liability.amount) || 0), 0);
                    }
                    guarantor.net_worth = guarantor.total_assets - guarantor.total_liabilities;
                });
                
                // Financial summary
                res.financial_summary = {
                    total_fees: res.fees.reduce((sum, fee) => sum + (parseFloat(fee.amount) || 0), 0),
                    total_repayments: res.repayments.reduce((sum, repayment) => sum + (parseFloat(repayment.amount) || 0), 0),
                    total_individual_borrower_assets: res.borrowers.reduce((sum, borrower) => sum + (borrower.total_assets || 0), 0),
                    total_individual_borrower_liabilities: res.borrowers.reduce((sum, borrower) => sum + (borrower.total_liabilities || 0), 0),
                    total_company_borrower_assets: res.company_borrowers.reduce((sum, company) => sum + (company.total_assets || 0), 0),
                    total_company_borrower_liabilities: res.company_borrowers.reduce((sum, company) => sum + (company.total_liabilities || 0), 0),
                    total_guarantor_assets: res.guarantors.reduce((sum, guarantor) => sum + (guarantor.total_assets || 0), 0),
                    total_guarantor_liabilities: res.guarantors.reduce((sum, guarantor) => sum + (guarantor.total_liabilities || 0), 0),
                };
            }
            
            return [null, res];
        }
    });
}

/**
 * Retrieves archived applications with pagination and filtering
 * @param {Object} params - Query parameters for filtering and pagination
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function archivedApplications(params) {
    return sendRequest({
        url: "/api/applications/applications/archived/",
        method: "get",
        params: params,
    });
}

/**
 * Retrieves statistics about archived applications
 * @returns {Promise} - Promise that resolves to [error, data]
 */
export function archivedApplicationsStats() {
    return sendRequest({
        url: "/api/applications/applications/archive_stats/",
        method: "get",
    });
}

export const applicationApi = {
    applications,
    application,
    addApplications,
    calculator,
    notes,
    addNote,
    updateStage,
    createApplicationWithCascade,
    deleteApplication,
    updateApplication,
    updateApplicationWithCascade,
    generatePdf,
    fees,
    assignBd,
    // Valuer functions
    valuers,
    addValuer,
    updateValuer,
    deactivateValuer,
    activateValuer,
    // Quantity Surveyor functions
    quantitySurveyors,
    addQuantitySurveyor,
    updateQuantitySurveyor,
    deactivateQuantitySurveyor,
    activateQuantitySurveyor,
    applicationWithCascade,
    // Archived applications functions
    archivedApplications,
    archivedApplicationsStats,
}