import sendRequest from '@/server/sendRequest';

export const productsApi = {
  // Get list of products with optional filters
  getProducts: async (params) => {
    return sendRequest({
      url: '/api/products/products/',
      method: 'get',
      params
    });
  },

  // Get a single product by ID
  getProduct: async (id) => {
    return sendRequest({
      url: `/api/products/products/${id}/`,
      method: 'get'
    });
  },

  // Create a new product
  createProduct: async (data) => {
    return sendRequest({
      url: '/api/products/products/',
      method: 'post',
      data
    });
  },

  // Update a product
  updateProduct: async (id, data) => {
    return sendRequest({
      url: `/api/products/products/${id}/`,
      method: 'put',
      data
    });
  },

  // Delete a product
  deleteProduct: async (id) => {
    return sendRequest({
      url: `/api/products/products/${id}/`,
      method: 'delete'
    });
  }
};
