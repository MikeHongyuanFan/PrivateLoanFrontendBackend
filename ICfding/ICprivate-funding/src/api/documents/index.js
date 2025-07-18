import sendRequest from '@/server/sendRequest';

export const documentsApi = {
  // Get list of documents with optional filters
  getDocuments: async (params) => {
    return sendRequest({
      url: '/api/documents/documents/',
      method: 'get',
      params
    });
  },

  // Get a single document by ID
  getDocument: async (id) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/`,
      method: 'get'
    });
  },

  // Download a document
  downloadDocument: async (id) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/download/`,
      method: 'get',
      responseType: 'blob'
    });
  },

  // Preview a document
  previewDocument: async (id) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/preview/`,
      method: 'get',
      responseType: 'blob'
    });
  },

  // Create a new document
  createDocument: async (formData) => {
    return sendRequest({
      url: '/api/documents/documents/',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Update a document
  updateDocument: async (id, formData) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/`,
      method: 'patch',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Create a new version of a document
  createDocumentVersion: async (id, formData) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/create-version/`,
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Delete a document
  deleteDocument: async (id) => {
    return sendRequest({
      url: `/api/documents/documents/${id}/`,
      method: 'delete'
    });
  },

  // Get list of applications
  getApplications: async (params) => {
    return sendRequest({
      url: '/api/applications/applications/',
      method: 'get',
      params
    });
  },

  // Get list of borrowers
  getBorrowers: async (params) => {
    return sendRequest({
      url: '/api/borrowers/borrowers/',
      method: 'get',
      params
    });
  },

  // Repayments
  repayments: () => sendRequest({
    url: '/api/documents/repayments/',
    method: 'get'
  }),

  repaymentCompliance: (params) => sendRequest({
    url: '/api/reports/repayment-compliance/',
    method: 'get',
    params
  }),

  updateRepayments: (id, file) => {
    const formData = new FormData()
    formData.append('invoice', file)
    return sendRequest({
      url: `/api/documents/repayments/${id}/`,
      method: 'put',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  deleteRepayment: (id) => sendRequest({
    url: `/api/documents/repayments/${id}/`,
    method: 'delete'
  }),

  markRepaymentAsPaid: (id) => sendRequest({
    url: `/api/documents/repayments/${id}/mark-paid/`,
    method: 'post'
  }),

  // Download a repayment invoice
  downloadRepaymentInvoice: (id) => sendRequest({
    url: `/api/documents/repayments/${id}/download_invoice/`,
    method: 'get',
    responseType: 'blob'
  }),

  // Preview a repayment invoice
  previewRepaymentInvoice: (id) => sendRequest({
    url: `/api/documents/repayments/${id}/preview_invoice/`,
    method: 'get',
    responseType: 'blob'
  })
};
