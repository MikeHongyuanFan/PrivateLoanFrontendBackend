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
    console.log("API call: application() with params:", params);
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
                
                // Ensure each guarantor has assets and liabilities
                res.guarantors.forEach(guarantor => {
                    guarantor.assets = guarantor.assets || [];
                    guarantor.liabilities = guarantor.liabilities || [];
                });
                
                // Ensure borrowers array exists
                res.borrowers = res.borrowers || [];
                
                // Ensure security_properties array exists
                res.security_properties = res.security_properties || [];
                
                // Ensure loan_requirements array exists
                res.loan_requirements = res.loan_requirements || [];
                
                // Ensure documents, notes, fees, repayments arrays exist
                res.documents = res.documents || [];
                res.notes = res.notes || [];
                res.fees = res.fees || [];
                res.repayments = res.repayments || [];
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
    generatePdf,
    fees,
    assignBd
}