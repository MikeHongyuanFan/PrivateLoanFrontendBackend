/**
 * Utility functions for handling API responses
 */

/**
 * Handles API responses by standardizing the format and handling errors
 * @param {Object} response - The response object from the API
 * @returns {Object} The processed response data
 * @throws {Error} If the response indicates an error
 */
export const handleResponse = (response) => {
  // Check if response exists
  if (!response) {
    throw new Error('No response received');
  }

  // If response has data property, return it
  if (response.data !== undefined) {
    // Check if the API returned an error
    if (response.data.error) {
      throw new Error(response.data.error.message || 'API error occurred');
    }
    return response.data;
  }

  // If response is the data itself
  return response;
};

/**
 * Creates an error response object
 * @param {string} message - Error message
 * @param {number} status - HTTP status code
 * @returns {Object} Error response object
 */
export const createErrorResponse = (message, status = 500) => {
  return {
    error: true,
    status,
    message,
  };
};

/**
 * Creates a success response object
 * @param {any} data - Response data
 * @param {number} status - HTTP status code
 * @returns {Object} Success response object
 */
export const createSuccessResponse = (data, status = 200) => {
  return {
    error: false,
    status,
    data,
  };
};
