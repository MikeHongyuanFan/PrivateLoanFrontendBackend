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

import ApiClient from '../ApiClient';
import Product from './Product';

/**
 * The PaginatedProductList model module.
 * @module models/PaginatedProductList
 * @version 1.0.0
 */
class PaginatedProductList {
    /**
     * Constructs a new <code>PaginatedProductList</code>.
     * @alias module:models/PaginatedProductList
     */
    constructor() { 
        
        PaginatedProductList.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>PaginatedProductList</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/PaginatedProductList} obj Optional instance to populate.
     * @return {module:models/PaginatedProductList} The populated <code>PaginatedProductList</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new PaginatedProductList();

            if (data.hasOwnProperty('count')) {
                obj['count'] = ApiClient.convertToType(data['count'], 'Number');
            }
            if (data.hasOwnProperty('next')) {
                obj['next'] = ApiClient.convertToType(data['next'], 'String');
            }
            if (data.hasOwnProperty('previous')) {
                obj['previous'] = ApiClient.convertToType(data['previous'], 'String');
            }
            if (data.hasOwnProperty('results')) {
                obj['results'] = ApiClient.convertToType(data['results'], [Product]);
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>PaginatedProductList</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>PaginatedProductList</code>.
     */
    static validateJSON(data) {
        // ensure the json data is a string
        if (data['next'] && !(typeof data['next'] === 'string' || data['next'] instanceof String)) {
            throw new Error("Expected the field `next` to be a primitive type in the JSON string but got " + data['next']);
        }
        // ensure the json data is a string
        if (data['previous'] && !(typeof data['previous'] === 'string' || data['previous'] instanceof String)) {
            throw new Error("Expected the field `previous` to be a primitive type in the JSON string but got " + data['previous']);
        }
        if (data['results']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['results'])) {
                throw new Error("Expected the field `results` to be an array in the JSON data but got " + data['results']);
            }
            // validate the optional field `results` (array)
            for (const item of data['results']) {
                Product.validateJSON(item);
            };
        }

        return true;
    }


}



/**
 * @member {Number} count
 */
PaginatedProductList.prototype['count'] = undefined;

/**
 * @member {String} next
 */
PaginatedProductList.prototype['next'] = undefined;

/**
 * @member {String} previous
 */
PaginatedProductList.prototype['previous'] = undefined;

/**
 * @member {Array.<module:models/Product>} results
 */
PaginatedProductList.prototype['results'] = undefined;






export default PaginatedProductList;

