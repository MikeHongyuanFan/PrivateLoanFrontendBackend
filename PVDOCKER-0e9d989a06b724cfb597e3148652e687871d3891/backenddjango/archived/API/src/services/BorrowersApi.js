/**
 * CRM Loan Management System API
 * A comprehensive CRM system for loan applications with fully synchronized frontend and backend development.
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */


import ApiClient from "../ApiClient";
import BorrowerDetail from '../models/BorrowerDetail';
import BorrowerDetailRequest from '../models/BorrowerDetailRequest';
import BorrowerFinancialSummary from '../models/BorrowerFinancialSummary';
import BorrowerGuarantor from '../models/BorrowerGuarantor';
import BorrowerGuarantorRequest from '../models/BorrowerGuarantorRequest';
import PaginatedBorrowerGuarantorList from '../models/PaginatedBorrowerGuarantorList';
import PaginatedBorrowerListList from '../models/PaginatedBorrowerListList';
import PatchedBorrowerDetailRequest from '../models/PatchedBorrowerDetailRequest';
import PatchedBorrowerGuarantorRequest from '../models/PatchedBorrowerGuarantorRequest';

/**
* Borrowers service.
* @module services/BorrowersApi
* @version 1.0.0
*/
export default class BorrowersApi {

    /**
    * Constructs a new BorrowersApi. 
    * @alias module:services/BorrowersApi
    * @class
    * @param {module:ApiClient} [apiClient] Optional API client implementation to use,
    * default to {@link module:ApiClient#instance} if unspecified.
    */
    constructor(apiClient) {
        this.apiClient = apiClient || ApiClient.instance;
    }


    /**
     * Callback function to receive the result of the borrowerGuarantorDetail operation.
     * @callback module:services/BorrowersApi~borrowerGuarantorDetailCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerGuarantor} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Number} id A unique integer value identifying this guarantor.
     * @param {module:services/BorrowersApi~borrowerGuarantorDetailCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerGuarantor}
     */
    borrowerGuarantorDetail(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowerGuarantorDetail");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerGuarantor;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/{id}/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersApplicationsRetrieve operation.
     * @callback module:services/BorrowersApi~borrowersApplicationsRetrieveCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get all applications for a borrower
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {module:services/BorrowersApi~borrowersApplicationsRetrieveCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersApplicationsRetrieve(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersApplicationsRetrieve");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/applications/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersCompanyList operation.
     * @callback module:services/BorrowersApi~borrowersCompanyListCallback
     * @param {String} error Error message, if any.
     * @param {module:models/PaginatedBorrowerListList} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * View for listing company borrowers
     * @param {Object} opts Optional parameters
     * @param {Number} [page] A page number within the paginated result set.
     * @param {module:services/BorrowersApi~borrowersCompanyListCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/PaginatedBorrowerListList}
     */
    borrowersCompanyList(opts, callback) {
      opts = opts || {};
      let postBody = null;

      let pathParams = {
      };
      let queryParams = {
        'page': opts['page']
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = PaginatedBorrowerListList;
      return this.apiClient.callApi(
        '/api/borrowers/company/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersCreate operation.
     * @callback module:services/BorrowersApi~borrowersCreateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Object} opts Optional parameters
     * @param {module:models/BorrowerDetailRequest} [borrowerDetailRequest] 
     * @param {module:services/BorrowersApi~borrowersCreateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersCreate(opts, callback) {
      opts = opts || {};
      let postBody = opts['borrowerDetailRequest'];

      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersDestroy operation.
     * @callback module:services/BorrowersApi~borrowersDestroyCallback
     * @param {String} error Error message, if any.
     * @param data This operation does not return a value.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {module:services/BorrowersApi~borrowersDestroyCallback} callback The callback function, accepting three arguments: error, data, response
     */
    borrowersDestroy(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersDestroy");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = [];
      let returnType = null;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/', 'DELETE',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersFinancialSummaryRetrieve operation.
     * @callback module:services/BorrowersApi~borrowersFinancialSummaryRetrieveCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerFinancialSummary} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get a financial summary for a borrower
     * @param {Number} id 
     * @param {module:services/BorrowersApi~borrowersFinancialSummaryRetrieveCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerFinancialSummary}
     */
    borrowersFinancialSummaryRetrieve(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersFinancialSummaryRetrieve");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerFinancialSummary;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/financial-summary/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsByBorrowerId operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsByBorrowerIdCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get all guarantors for a borrower
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {module:services/BorrowersApi~borrowersGuarantorsByBorrowerIdCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersGuarantorsByBorrowerId(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersGuarantorsByBorrowerId");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/guarantors/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsCreate operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsCreateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerGuarantor} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Object} opts Optional parameters
     * @param {module:models/BorrowerGuarantorRequest} [borrowerGuarantorRequest] 
     * @param {module:services/BorrowersApi~borrowersGuarantorsCreateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerGuarantor}
     */
    borrowersGuarantorsCreate(opts, callback) {
      opts = opts || {};
      let postBody = opts['borrowerGuarantorRequest'];

      let pathParams = {
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerGuarantor;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/', 'POST',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsDestroy operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsDestroyCallback
     * @param {String} error Error message, if any.
     * @param data This operation does not return a value.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Number} id A unique integer value identifying this guarantor.
     * @param {module:services/BorrowersApi~borrowersGuarantorsDestroyCallback} callback The callback function, accepting three arguments: error, data, response
     */
    borrowersGuarantorsDestroy(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersGuarantorsDestroy");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = [];
      let returnType = null;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/{id}/', 'DELETE',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsGuaranteedApplicationsRetrieve operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsGuaranteedApplicationsRetrieveCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerGuarantor} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * Get all applications guaranteed by a guarantor
     * @param {Number} id A unique integer value identifying this guarantor.
     * @param {module:services/BorrowersApi~borrowersGuarantorsGuaranteedApplicationsRetrieveCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerGuarantor}
     */
    borrowersGuarantorsGuaranteedApplicationsRetrieve(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersGuarantorsGuaranteedApplicationsRetrieve");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerGuarantor;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/{id}/guaranteed_applications/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsList operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsListCallback
     * @param {String} error Error message, if any.
     * @param {module:models/PaginatedBorrowerGuarantorList} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Object} opts Optional parameters
     * @param {Number} [application] 
     * @param {Number} [borrower] 
     * @param {module:models/String} [guarantorType] * `individual` - Individual * `company` - Company
     * @param {Number} [page] A page number within the paginated result set.
     * @param {String} [search] A search term.
     * @param {module:services/BorrowersApi~borrowersGuarantorsListCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/PaginatedBorrowerGuarantorList}
     */
    borrowersGuarantorsList(opts, callback) {
      opts = opts || {};
      let postBody = null;

      let pathParams = {
      };
      let queryParams = {
        'application': opts['application'],
        'borrower': opts['borrower'],
        'guarantor_type': opts['guarantorType'],
        'page': opts['page'],
        'search': opts['search']
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = PaginatedBorrowerGuarantorList;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsPartialUpdate operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsPartialUpdateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerGuarantor} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Number} id A unique integer value identifying this guarantor.
     * @param {Object} opts Optional parameters
     * @param {module:models/PatchedBorrowerGuarantorRequest} [patchedBorrowerGuarantorRequest] 
     * @param {module:services/BorrowersApi~borrowersGuarantorsPartialUpdateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerGuarantor}
     */
    borrowersGuarantorsPartialUpdate(id, opts, callback) {
      opts = opts || {};
      let postBody = opts['patchedBorrowerGuarantorRequest'];
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersGuarantorsPartialUpdate");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerGuarantor;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/{id}/', 'PATCH',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersGuarantorsUpdate operation.
     * @callback module:services/BorrowersApi~borrowersGuarantorsUpdateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerGuarantor} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing guarantors
     * @param {Number} id A unique integer value identifying this guarantor.
     * @param {Object} opts Optional parameters
     * @param {module:models/BorrowerGuarantorRequest} [borrowerGuarantorRequest] 
     * @param {module:services/BorrowersApi~borrowersGuarantorsUpdateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerGuarantor}
     */
    borrowersGuarantorsUpdate(id, opts, callback) {
      opts = opts || {};
      let postBody = opts['borrowerGuarantorRequest'];
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersGuarantorsUpdate");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerGuarantor;
      return this.apiClient.callApi(
        '/api/borrowers/guarantors/{id}/', 'PUT',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersList operation.
     * @callback module:services/BorrowersApi~borrowersListCallback
     * @param {String} error Error message, if any.
     * @param {module:models/PaginatedBorrowerListList} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Object} opts Optional parameters
     * @param {Boolean} [hasApplications] 
     * @param {module:models/String} [maritalStatus] * `single` - Single * `married` - Married * `de_facto` - De Facto * `divorced` - Divorced * `widowed` - Widowed
     * @param {String} [ordering] Which field to use when ordering the results.
     * @param {Number} [page] A page number within the paginated result set.
     * @param {module:models/String} [residencyStatus] * `citizen` - Citizen * `permanent_resident` - Permanent Resident * `temporary_resident` - Temporary Resident * `foreign_investor` - Foreign Investor
     * @param {String} [search] A search term.
     * @param {module:services/BorrowersApi~borrowersListCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/PaginatedBorrowerListList}
     */
    borrowersList(opts, callback) {
      opts = opts || {};
      let postBody = null;

      let pathParams = {
      };
      let queryParams = {
        'has_applications': opts['hasApplications'],
        'marital_status': opts['maritalStatus'],
        'ordering': opts['ordering'],
        'page': opts['page'],
        'residency_status': opts['residencyStatus'],
        'search': opts['search']
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = PaginatedBorrowerListList;
      return this.apiClient.callApi(
        '/api/borrowers/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersPartialUpdate operation.
     * @callback module:services/BorrowersApi~borrowersPartialUpdateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {Object} opts Optional parameters
     * @param {module:models/PatchedBorrowerDetailRequest} [patchedBorrowerDetailRequest] 
     * @param {module:services/BorrowersApi~borrowersPartialUpdateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersPartialUpdate(id, opts, callback) {
      opts = opts || {};
      let postBody = opts['patchedBorrowerDetailRequest'];
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersPartialUpdate");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/', 'PATCH',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersRetrieve operation.
     * @callback module:services/BorrowersApi~borrowersRetrieveCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {module:services/BorrowersApi~borrowersRetrieveCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersRetrieve(id, callback) {
      let postBody = null;
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersRetrieve");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = [];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/', 'GET',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }

    /**
     * Callback function to receive the result of the borrowersUpdate operation.
     * @callback module:services/BorrowersApi~borrowersUpdateCallback
     * @param {String} error Error message, if any.
     * @param {module:models/BorrowerDetail} data The data returned by the service call.
     * @param {String} response The complete HTTP response.
     */

    /**
     * API endpoint for managing borrowers
     * @param {Number} id A unique integer value identifying this borrower.
     * @param {Object} opts Optional parameters
     * @param {module:models/BorrowerDetailRequest} [borrowerDetailRequest] 
     * @param {module:services/BorrowersApi~borrowersUpdateCallback} callback The callback function, accepting three arguments: error, data, response
     * data is of type: {@link module:models/BorrowerDetail}
     */
    borrowersUpdate(id, opts, callback) {
      opts = opts || {};
      let postBody = opts['borrowerDetailRequest'];
      // verify the required parameter 'id' is set
      if (id === undefined || id === null) {
        throw new Error("Missing the required parameter 'id' when calling borrowersUpdate");
      }

      let pathParams = {
        'id': id
      };
      let queryParams = {
      };
      let headerParams = {
      };
      let formParams = {
      };

      let authNames = ['jwtAuth', 'Bearer'];
      let contentTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
      let accepts = ['application/json'];
      let returnType = BorrowerDetail;
      return this.apiClient.callApi(
        '/api/borrowers/{id}/', 'PUT',
        pathParams, queryParams, headerParams, formParams, postBody,
        authNames, contentTypes, accepts, returnType, null, callback
      );
    }


}
